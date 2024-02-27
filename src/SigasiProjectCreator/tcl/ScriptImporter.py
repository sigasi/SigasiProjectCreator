"""
    :copyright: (c) 2008-2024 Sigasi
    :license: BSD, see LICENSE for more details.
"""

from dataclasses import dataclass
import pathlib
import re
import sys
import tkinter
from SigasiProjectCreator import abort_if_false
from SigasiProjectCreator import VhdlVersion

from SigasiProjectCreator.ProjectFileParser import ProjectFileParser, project_file_parser, ProjectFileParserResult
from SigasiProjectCreator.VhdlVersion import get_vhdl_version


@project_file_parser(['tcl'])
class ScriptImporter(ProjectFileParser):
    """Script"""
    def __init__(self):
        super().__init__()
        self.parser_line_types = {
            "VHDL": self.parse_vhdl_line,
            "VLOG": self.parse_vlog_line
        }

    def parse_tkinter(self, tcl_file, options):
        tcl_engine = tkinter.Tcl()
        ignore_commands = ['vlib', 'vsim', 'vmap', 'echo', 'run', 'onerror', 'quietly', 'add']
        if options.tcl_ignore:
            ignore_commands.extend(options.tcl_ignore)

        tcl_script = ['set result ""',
                      'proc vcom {args} { global result; set result [ string cat $result "SIGASI VHDL $args\n"] }',
                      'proc vlog {args} { global result; set result [ string cat $result "SIGASI VLOG $args\n"] }']
        for ignore_command in ignore_commands:
            if options.verbose:
                tcl_script.append('proc ' + ignore_command
                                  + ' {args} { puts "SIGASI IGNORE [lindex [info level 0] 0] $args" }')
            else:
                tcl_script.append('proc ' + ignore_command + ' {args} {}')
        tcl_script.append("""
            proc alias {name args} {
                global alias_code
                dict set alias_code $name $args
                proc $name {} {
                    global alias_code
                    set my_name [lindex [info level 0] 0]
                    set comstring [dict get $alias_code $my_name]
                    foreach line [ split $comstring "\\n" ] {
                        if {[string length $line] > 1} {
                            eval $line
                        }
                    }
                }
            }
        """)
        if tcl_file.strip():
            tcl_script.append(f'source {tcl_file.strip()}')
        tcl_script.append(options.tcl_run_command)
        tcl_script.append("return $result")
        return tcl_engine.eval("\n".join(tcl_script))

    def parse_file(self, tcl_file, options=None):
        library_mapping = dict()
        includes = set()
        defines = []

        tcl_result = self.parse_tkinter(tcl_file, options)

        if options and options.verbose:
            print(f'tcl returned:\n{tcl_result}')

        for line in tcl_result.splitlines():
            if len(line.strip()) < 1:
                continue
            if not line.startswith("SIGASI "):
                if options and options.verbose:
                    print(f'TCL parser: ignoring {line}')
                continue
            line = line[7:]
            line_type = line.split()[0]
            abort_if_false(line_type in self.parser_line_types.keys(), f'unsupported line type {line_type}')
            line_parser = self.parser_line_types[line_type]
            line_files, line_library, line_version, line_defines, line_includes = line_parser(line, options)
            for file in line_files:
                # TODO handle wildcards and environment variables... future work
                library_mapping[pathlib.Path(file).absolute().resolve()] = line_library or options.work_lib
            # TODO handle VHDL version - future work
            if line_defines:
                defines.extend(line_defines)
            if line_includes:
                includes.update(line_includes)

        return ProjectFileParserResult(library_mapping, verilog_defines=defines, verilog_includes=includes)
    
    def parse_vhdl_line(self, line, options):
        vhdl_version = None
        vhdl_files = []
        vhdl_library = None
        expect_library = False
        for element in line.split():
            if expect_library:
                vhdl_library = element
                expect_library = False
            elif element == '-work':
                expect_library = True
            elif element.split('.')[-1] in ['vhd', 'vhdl'] or element.endswith('*'):
                vhdl_files.append(element)
            elif re.match('.*[0-9][0-9]$', element):
                vhdl_version = get_vhdl_version(element)
        if options and options.verbose:
            print(f'VHDL: {vhdl_files} : {vhdl_library} {vhdl_version}')
        return vhdl_files, vhdl_library, vhdl_version, None, None

    def parse_vlog_line(self, line, options):
        verilog_files = []
        verilog_library = None
        expect_library = False
        verilog_defines = []
        expect_define = False
        verilog_includes = set()
        for element in line.split():
            if expect_library:
                # TODO handle environment variables
                verilog_library = element
                expect_library = False
            elif expect_define:
                # TODO handle environment variables
                verilog_defines.append(element)
                expect_define = False
            elif element == '-work':
                expect_library = True
            elif element == '-define':
                expect_define = True
            elif element.split('.')[-1] in ['v', 'sv'] or element.endswith('*'):
                verilog_files.append(element)
            elif element.startswith('+incdir+'):
                verilog_includes.add(pathlib.Path(element[8:]).absolute().resolve())
            elif element.startswith('+define+'):
                verilog_defines.append(element[8:])
        if options and options.verbose:
            print(f'VLOG: {verilog_files} : {verilog_library} ## {verilog_defines} {verilog_includes}')
        return verilog_files, verilog_library, None, verilog_defines, verilog_includes


# A data class to pass some options for ad-hoc command line testing.
@dataclass
class ScriptImporterOptions:
    vhdl_version: str
    verbose: bool
    tcl_run_command: str
    work_lib: str
    input_file: str
        

def main(args):
    options = ScriptImporterOptions(
        verbose=True,
        vhdl_version=VhdlVersion.TWENTY_O_EIGHT,
        tcl_run_command=args[1] if len(args)>1 else '',
        work_lib='work',
        input_file=args[0]
    )

    parser_output = ScriptImporter().parse_file(args[0], options)
    print(f'Library mapping:\n{parser_output.library_mapping}')
    print(f'Defines:\n{parser_output.verilog_defines}')
    print(f'Includes:\n{parser_output.verilog_includes}')


if __name__ == '__main__':
    main(sys.argv[1:])
