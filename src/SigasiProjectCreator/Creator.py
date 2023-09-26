# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2008-2023 Sigasi
    :license: BSD, see LICENSE for more details.
"""
import os
import re
import pathlib
from string import Template

from SigasiProjectCreator import absnormpath, posixpath
from SigasiProjectCreator import VhdlVersion
from SigasiProjectCreator import VerilogVersion
from SigasiProjectCreator import SettingsFileWriter
from SigasiProjectCreator.ArgsAndFileParser import ArgsAndFileParser

__VERSION_ERROR = Template('''Only ${versions} is/are allowed as ${lang} version number.''')


def check_hdl_versions(vhdl_version, verilog_version):
    verilog_error = ""
    vhdl_error = ""
    verilog_versions = ", ".join([str(v) for v in VerilogVersion.get_enums()])
    vhdl_versions = ", ".join([str(v) for v in VhdlVersion.get_enums()])
    if vhdl_version is None and verilog_version is None:
        vhdl_error = __VERSION_ERROR.substitute(versions=vhdl_versions, lang="VHDL")
        verilog_error = __VERSION_ERROR.substitute(versions=verilog_versions, lang="Verilog")
    if vhdl_version is not None and vhdl_version not in VhdlVersion.get_enums():
        vhdl_error = __VERSION_ERROR.substitute(versions=vhdl_versions, lang="VHDL")
    if verilog_version is not None and verilog_version not in VerilogVersion.get_enums():
        verilog_error = __VERSION_ERROR.substitute(versions=verilog_versions, lang="Verilog")
    if vhdl_error or verilog_error:
        raise ValueError("\n".join(filter(None, [vhdl_error, verilog_error])))


def get_settings_folder(destination: pathlib.Path, suffix=None):
    if suffix:
        settings_folder = destination.joinpath(suffix)
    else:
        settings_folder = destination
    if settings_folder.exists():
        assert settings_folder.is_dir(), f'*ERROR* Settings folder {settings_folder} exists but is not a folder'
        return settings_folder
    assert settings_folder.parent.is_dir(), f'*ERROR* Cannot create settings folder {settings_folder}, parent is not'\
                                            'an existing folder'
    settings_folder.mkdir()
    return settings_folder


class LibraryMappingFileCreator:
    """A Library Mapping File Creator helps you to easily create a Sigasi Library Mapping file.

    If you know which VHDL or Verilog version is being used you can pass it to the constructor.
    See VhdlVersion and VerilogVersion for this.

    You can add library mappings by calling the add_mapping method.
    To create the .library_mapping file content, simply call str() of your LibraryMappingFileCreator instance.

    Typical example:
        creator = LibraryMappingFileCreator()
        creator.add_mapping("test.vhd", "myLib")
        creator.add_mapping("Copy_of_test.vhd", "not mapped")
        return str(creator)

    """
    __LIBRARIES_TEMPLATE = Template(
        '''<?xml version="1.0" encoding="UTF-8"?>
<com.sigasi.hdt.vhdl.scoping.librarymapping.model:LibraryMappings xmlns:com.sigasi.hdt.vhdl.scoping.librarymapping.model="com.sigasi.hdt.vhdl.scoping.librarymapping" Version="2">
$mappings</com.sigasi.hdt.vhdl.scoping.librarymapping.model:LibraryMappings>
''')

    __MAPPING_TEMPLATE = Template('  <Mappings Location="$path" Library="$library"/>\n')

    __DEFAULT_VERILOG_MAPPINGS = {
    }

    __DEFAULT_VHDL_MAPPINGS = {
        "Common Libraries/IEEE": "ieee",
        "Common Libraries/IEEE Synopsys": "ieee",
        "Common Libraries": "not mapped",
        "Common Libraries/STD": "std",
    }

    def __init__(self):
        self.__entries = dict()
        self.__vhdl_version = None
        self.__verilog_version = None

    def set_languages(self, vhdl_version, verilog_version):
        self.__vhdl_version = vhdl_version
        self.__verilog_version = verilog_version
        self.__add_default_mappings()

    def __add_default_mappings(self):
        # Default value
        self.add_mapping("", "not mapped")
        if self.__vhdl_version is not None:
            for path, library in self.__DEFAULT_VHDL_MAPPINGS.items():
                self.add_mapping(path, library)
        if self.__verilog_version is not None:
            for path, library in self.__DEFAULT_VERILOG_MAPPINGS.items():
                self.add_mapping(path, library)

    def __str__(self):
        mappings = ""
        for (path, library) in sorted(self.__entries.items()):
            mappings += self.__MAPPING_TEMPLATE.substitute(
                    path=path,
                    library=library)
        return self.__LIBRARIES_TEMPLATE.substitute(mappings=mappings)

    def add_mapping(self, path, library=None):
        if library is None:
            self.__entries[path] = 'not mapped'
        self.__entries[path] = library

    def get_mapping(self, path):
        result = None
        if path in self.__entries:
            result = self.__entries[path]
            if result == 'not mapped':
                result = None
        return result

    def unmap(self, path):
        self.__entries[path] = "not mapped"

    def remove_mapping(self, path):
        del self.__entries[path]

    def write(self, destination):
        SettingsFileWriter.write(destination, ".library_mapping.xml", str(self))


class ProjectFileCreator:
    """A Project File Creator helps you to easily create a Sigasi Project file.

    You can specify the VHDL version (see VhdlVersion.py) in the constructor.

    You can add linked resources to your project by calling the add_link method.
    To create the .project file, simply call str() of your ProjectFileCreator instance.

    Typical example:
        creator = ProjectFileCreator(project_name)
        creator.add_link("test.vhd", "/home/heeckhau/shared/test.vhd")
        creator.write("/home/heeckhau/test/")

    """

    __LINK_TEMPLATE = Template(
'''\t\t<link>
\t\t\t<name>${name}</name>
\t\t\t<type>${link_type}</type>
\t\t\t<${loc_type}>${location}</${loc_type}>
\t\t</link>
''')

    __PROJECT_REFERENCE_TEMPLATE = Template("""\t\t<project>$name</project>\n""")

    __VHDL_NATURE = "\t\t<nature>com.sigasi.hdt.vhdl.ui.vhdlNature</nature>\n"
    __VERILOG_NATURE = "\t\t<nature>com.sigasi.hdt.verilog.ui.verilogNature</nature>\n"
    __VUNIT_NATURE = "\t\t<nature>com.sigasi.hdt.toolchains.vunit.nature</nature>\n"
    __VUNIT_BUILDSPEC = '''\t\t<buildCommand>
\t\t\t<name>com.sigasi.hdt.toolchains.vunit.builder</name>
\t\t\t<arguments>
\t\t\t</arguments>
\t\t</buildCommand>\n'''

    __PROJECT_FILE_TEMPLATE = Template(
'''<?xml version="1.0" encoding="UTF-8"?>
<projectDescription>
\t<name>${project_name}</name>
\t<comment></comment>
\t<projects>
${project_references}\t</projects>
\t<buildSpec>
${buildspecs}\t\t<buildCommand>
\t\t\t<name>org.eclipse.xtext.ui.shared.xtextBuilder</name>
\t\t\t<arguments>
\t\t\t</arguments>
\t\t</buildCommand>
\t</buildSpec>
\t<natures>
${natures}\t\t<nature>org.eclipse.xtext.ui.shared.xtextNature</nature>
\t</natures>
\t<linkedResources>
${links}\t</linkedResources>
</projectDescription>
''')

    __DEFAULT_LINKS = [
        ["Common Libraries", Template("virtual:/virtual")],
        ["Common Libraries/IEEE", Template("sigasiresource:/vhdl/${version}/IEEE")],
        ["Common Libraries/IEEE Synopsys", Template("sigasiresource:/vhdl/${version}/IEEE%20Synopsys")],
        ["Common Libraries/STD", Template("sigasiresource:/vhdl/${version}/STD")],
    ]

    def __init__(self, project_name):
        self.__project_name = project_name
        self.__links = []
        self.__project_references = []
        self.vhdl_version = None
        self.verilog_version = None
        self.force_vunit = None

    def set_languages(self, vhdl_version, verilog_version):
        self.vhdl_version = vhdl_version
        self.verilog_version = verilog_version
        if vhdl_version is not None:
            self.__add_default_links()

    def is_vunit(self):
        if self.force_vunit is not None:
            return self.force_vunit
        return False

    def __add_default_links(self):
        for name, template in self.__DEFAULT_LINKS:
            self.__links.append([name, template.substitute(version=self.vhdl_version), True, False])

    def __str__(self):
        links = ""
        project_references = ""
        buildspecs = ""
        natures = ""
        for [name, location, folder, is_path] in self.__links:
            location_type = "location" if (is_path and not str(location).startswith('virtual')) else "locationURI"
            links += self.__LINK_TEMPLATE.substitute(
                        name=name,
                        link_type=2 if folder else 1,
                        loc_type=location_type,
                        location=location)

        if self.verilog_version is not None:
            natures += self.__VERILOG_NATURE

        if self.vhdl_version is not None:
            natures += self.__VHDL_NATURE

        if self.is_vunit():
            buildspecs += self.__VUNIT_BUILDSPEC
            natures += self.__VUNIT_NATURE

        for project_reference in self.__project_references:
            project_references += self.__PROJECT_REFERENCE_TEMPLATE.substitute(
                name=project_reference)

        return self.__PROJECT_FILE_TEMPLATE.substitute(
            project_name=self.__project_name,
            project_references=project_references,
            buildspecs=buildspecs,
            natures=natures,
            links=links
        )

    def add_link(self, name, location, folder=False):
        if str(location).startswith('virtual'):
            self.__links.append([name, location, folder, False])
        else:
            # if name.startswith(".."):
            #     raise ValueError('invalid name "' + name + '", a name can not start with dots')
            self.__links.append([name, project_location_path(location), folder, True])

    def add_project_reference(self, name):
        self.__project_references.append(name)

    def write(self, destination, force_vunit=None):
        self.force_vunit = force_vunit
        SettingsFileWriter.write(destination, ".project", str(self))


class ProjectVersionCreator:
    """A ProjectVersionCreator helps you to create a .settings folder with the correct version files.
    It will create a "com.sigasi.hdt.vhdl.version.prefs" and a "com.sigasi.hdt.verilog.version.prefs" file in the
    ".settings" folder if a VHDL and/or Verilog version was given or if it doesn't yet exist.

    Typical example:
    creator = SigasiProjectCreator(VhdlVersion.NINETY_THREE)
    creator.write("/home/heeckhau/test/")
    """

    def __init__(self, version=VhdlVersion.NINETY_THREE):
        check_hdl_versions(version if version in VhdlVersion.get_enums() else None,
                           version if version in VerilogVersion.get_enums() else None)
        self.version = version
        self.lang = "vhdl" if self.version in VhdlVersion.get_enums() else "verilog"

    def write(self, destination):
        self.write_version(destination)

    def get_vhdl_version(self):
        if self.lang == 'vhdl':
            return self.version
        return None

    def get_verilog_version(self):
        if self.lang == 'verilog':
            return self.version
        return None

    def __str__(self):
        return "<project>={0}".format(self.version)

    def write_version(self, destination):
        settings_dir = get_settings_folder(destination, '.settings')
        version_file_path = "com.sigasi.hdt.{0}.version.prefs".format(self.lang)
        if self.version is not None:
            SettingsFileWriter.write(settings_dir, version_file_path, str(self))


class ProjectPreferencesCreator:
    """A ProjectPreferencesCreator helps you to create a .settings folder with a Verilog preferences file.
    It will create a "com.sigasi.hdt.verilog.Verilog.prefs" file in the
    ".settings" folder if Verilog preferences were given or if it doesn't yet exist.

    Limitation: only Verilog supported atm
    """
    def __init__(self, language, verilog_includes, verilog_defines):
        self.verilog_includes = verilog_includes
        self.verilog_defines = verilog_defines
        self.lang = language

    def write(self, destination):
        settings_dir = get_settings_folder(destination, '.settings')
        prefs_file_path = "com.sigasi.hdt.{0}.{1}.prefs".format(self.lang, str(self.lang).title())
        SettingsFileWriter.write(settings_dir, prefs_file_path, str(self))

    def __str__(self):
        includes_string = ""
        defines_string = ""
        if self.lang == 'verilog' and self.verilog_includes is not None and len(self.verilog_includes) > 0:
            if isinstance(self.verilog_includes, list) and list:
                includes_string = "includePath="
                first = True
                for include_folder in self.verilog_includes:
                    if not first:
                        includes_string += ";"
                    first = False
                    includes_string += posixpath(include_folder)
                includes_string += "\n"
        if self.lang == 'verilog' and self.verilog_defines is not None and len(self.verilog_defines) > 0:
            defines_string = "propertiesDefine="
            for definition in self.verilog_defines:
                defines_string += "`define " + definition.replace('=',' ') + "\\r\\n"
            defines_string += "\n"
        return "eclipse.preferences.version=1\n" + includes_string + defines_string


class ProjectEncodingCreator:
    """
    Create <project dir>/.settings/com.sigasi.hdt.vhdl.version.prefs
    with file encoding settings (default UTF-8)
    """
    def __init__(self, encoding='UTF-8'):
        self.encoding = encoding

    def write(self, destination):
        settings_dir = get_settings_folder(destination, '.settings')
        prefs_file_path = "org.eclipse.core.resources.prefs"
        SettingsFileWriter.write(settings_dir, prefs_file_path, str(self))

    def __str__(self):
        return f'eclipse.preferences.version=1\nencoding/<project>={self.encoding}\n'


class VUnitPreferencesCreator:
    """ Help to write a .settings file for the VUnit script (run.py) location
    """
    def __init__(self, vunit_script="run.py"):
        self.script = vunit_script

    def write(self, destination):
        settings_dir = get_settings_folder(destination, '.settings')
        prefs_file_path = "com.sigasi.hdt.toolchains.vunit.prefs"
        SettingsFileWriter.write(settings_dir, prefs_file_path, str(self))
    
    def __str__(self):
        script_string = "VUnitScriptLocation=" + self.script
        return script_string + "\n" + "eclipse.preferences.version=1\n"


class SigasiProjectCreator:
    """This class helps you to easily create a Sigasi project (".project")
    and library mapping (".library_mapping.xml") file.
    It will also create a .settings folder if it doesn't yet exist, see ProjectVersionCreator.

    Typical example:
        creator = SigasiProjectCreator(project_name, VhdlVersion.NINETY_THREE)
        creator.add_link("test.vhd", "/home/heeckhau/shared/test.vhd")
        creator.add_mapping("test.vhd", "myLib")
        creator.set_languages(True, False)  # for a VHDL only project
        creator.write("/home/heeckhau/test/")
    """

    def __init__(self, project_name):
        self.__libraryMappingFileCreator = LibraryMappingFileCreator()
        self.__projectFileCreator = ProjectFileCreator(project_name)
        self.verilog_includes = []
        self.vhdl_version = None
        self.verilog_version = None
        self.languages_initialized = False

    def set_languages(self, has_vhdl, has_verilog):
        has_vhdl = has_vhdl or ArgsAndFileParser.get_enable_vhdl()
        has_verilog = has_verilog or ArgsAndFileParser.get_enable_verilog()
        if has_vhdl:
            self.vhdl_version = ArgsAndFileParser.get_vhdl_version()
        if has_verilog:
            self.verilog_version = ArgsAndFileParser.get_verilog_version()
        check_hdl_versions(self.vhdl_version, self.verilog_version)
        self.__projectFileCreator.set_languages(self.vhdl_version, self.verilog_version)
        self.__libraryMappingFileCreator.set_languages(self.vhdl_version, self.verilog_version)
        self.languages_initialized = True

    def add_link(self, name, location, folder=False):
        if folder and (location is None):
            # virtual folder
            self.__projectFileCreator.add_link(name, 'virtual:/virtual', folder)
        else:
            self.__projectFileCreator.add_link(name, posixpath(location), folder)

    def add_mapping(self, path, library):
        self.__libraryMappingFileCreator.add_mapping(posixpath(path), library)

    def remove_mapping(self, path):
        self.__libraryMappingFileCreator.remove_mapping(posixpath(path))

    def unmap(self, path):
        self.__libraryMappingFileCreator.unmap(posixpath(path))

    def get_mapping(self, path):
        return self.__libraryMappingFileCreator.get_mapping(path)

    def add_verilog_include(self, path):
        self.verilog_includes.append(path)

    def write(self, destination, verilog_includes=None, verilog_defines=None, force_vunit=None):
        assert self.languages_initialized, "HDL languages must be set before writing the project"

        if not isinstance(destination, pathlib.Path):
            destination = pathlib.Path(destination)

        self.__projectFileCreator.write(destination, force_vunit)
        self.__libraryMappingFileCreator.write(destination)
        if self.vhdl_version is not None:
            ProjectVersionCreator(ArgsAndFileParser.get_vhdl_version()).write(destination)
        if self.verilog_version is not None:
            ProjectVersionCreator(ArgsAndFileParser.get_verilog_version()).write(destination)
        self.verilog_includes.extend(verilog_includes or [])
        if self.verilog_includes or verilog_defines:
            verilog_prefs = ProjectPreferencesCreator('verilog', self.verilog_includes, verilog_defines)
            verilog_prefs.write(destination)
        if force_vunit:
            vunit_prefs = VUnitPreferencesCreator()
            vunit_prefs.write(destination)
        encoding_prefs = ProjectEncodingCreator(ArgsAndFileParser.get_encoding())
        encoding_prefs.write(destination)

    def add_unisim(self, unisim_location):
        self.add_link("Common Libraries/unisim", unisim_location, True)
        self.add_mapping("Common Libraries/unisim", "unisim")
        self.unmap("Common Libraries/unisim/primitive")
        self.unmap("Common Libraries/unisim/secureip")
        self.unmap("Common Libraries/unisim/retarget")
        self.unmap("Common Libraries/unisim/retarget_VCOMP.vhd")
        self.unmap("Common Libraries/unisim/unisim_retarget_VCOMP.vhd")

    def add_unimacro(self, unimacro_location):
        self.add_link("Common Libraries/unimacro", unimacro_location, True)
        self.add_mapping("Common Libraries/unimacro/unimacro_VCOMP.vhd", "unimacro")

    def add_project_reference(self, name):
        self.__projectFileCreator.add_project_reference(name)

    def add_uvm(self, uvm_location: pathlib.Path, uvm_library):
        if uvm_location is not None:
            self.add_link('Common Libraries/uvm', uvm_location.joinpath('src'), True)
            self.add_mapping('Common Libraries/uvm/uvm_pkg.sv', uvm_library)
            self.add_verilog_include('Common Libraries/uvm')


def project_location_path(my_path):
    assert (not (str(my_path).startswith('PROJECT') or str(my_path).startswith('PARENT-'))),\
        f'*OOPS* not expecting {my_path} here'
    if pathlib.Path(my_path).is_absolute():
        return my_path
    parent_level = 0
    while my_path.startswith('..'):
        parent_level += 1
        my_path = my_path[3::]
    if parent_level == 0:
        return 'PROJECT_LOC/' + my_path
    return 'PARENT-' + str(parent_level) + '-PROJECT_LOC/' + my_path
