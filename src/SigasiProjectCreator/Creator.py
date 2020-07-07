# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2008-2017 Sigasi
    :license: BSD, see LICENSE for more details.
"""
import os
import re
from string import Template

from SigasiProjectCreator import VhdlVersion
from SigasiProjectCreator import VerilogVersion
from SigasiProjectCreator import SettingsFileWriter


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
        "": "not mapped"
    }

    __DEFAULT_VHDL_MAPPINGS = {
        "Common Libraries/IEEE": "ieee",
        "Common Libraries/IEEE Synopsys": "ieee",
        "Common Libraries": "not mapped",
        "Common Libraries/STD": "std",
        "": "not mapped"
    }

    def __init__(self, vhdl_version=VhdlVersion.NINETY_THREE, verilog_version=None):
        self.__entries = dict()
        self.__add_default_mappings()

        check_hdl_versions(vhdl_version, verilog_version)
        self.__vhdl_version = vhdl_version
        self.__verilog_version = verilog_version

    def __add_default_mappings(self):
        if VhdlVersion is not None:
            for path, library in self.__DEFAULT_VHDL_MAPPINGS.items():
                self.add_mapping(path, library)
        if VerilogVersion is not None:
            for path, library in self.__DEFAULT_VERILOG_MAPPINGS.items():
                self.add_mapping(path, library)
        if VhdlVersion is None and VerilogVersion is None:
            # Default value
            self.add_mapping("", "not mapped")

    def __str__(self):
        mappings = ""
        for (path, library) in sorted(self.__entries.items()):
            mappings += self.__MAPPING_TEMPLATE.substitute(
                    path=path,
                    library=library)
        return self.__LIBRARIES_TEMPLATE.substitute(mappings=mappings)

    def add_mapping(self, path, library):
        self.__entries[path] = library

    def unmap(self, path):
        self.__entries[path] = "not mapped"

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

    __PROJECT_FILE_TEMPLATE = Template(
'''<?xml version="1.0" encoding="UTF-8"?>
<projectDescription>
\t<name>${project_name}</name>
\t<comment></comment>
\t<projects>
${project_references}\t</projects>
\t<buildSpec>
\t\t<buildCommand>
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

    def __init__(self, project_name, vhdl_version=VhdlVersion.NINETY_THREE, verilog_version=None):
        check_hdl_versions(vhdl_version, verilog_version)
        self.__project_name = project_name
        self.__version = vhdl_version
        self.__links = []
        self.__project_references = []
        self.__add_default_links()

    def is_verilog(self):
        vl_ext = re.compile("\.sv[hi]?$|\.v[h]?$", re.IGNORECASE)
        return any([vl_ext.search(l[1]) for l in self.__links])

    def is_vhdl(self):
        vhdl_ext = re.compile("\.vhd[l]?$", re.IGNORECASE)
        # VHDL is the default
        return not self.is_verilog() or any([vhdl_ext.search(l[1]) for l in self.__links])

    def __add_default_links(self):
        for name, template in self.__DEFAULT_LINKS:
            self.__links.append([name, template.substitute(version=self.__version), True, False])

    def __str__(self):
        links = ""
        project_references = ""
        natures = ""
        for [name, location, folder, is_path] in self.__links:
            location_type = "location" if is_path else "locationURI"
            links += self.__LINK_TEMPLATE.substitute(
                        name=name,
                        link_type=2 if folder else 1,
                        loc_type=location_type,
                        location=location)

        if self.is_verilog():
            natures += self.__VERILOG_NATURE

        if self.is_vhdl():
            natures += self.__VHDL_NATURE

        for project_reference in self.__project_references:
            project_references += self.__PROJECT_REFERENCE_TEMPLATE.substitute(
                name=project_reference)

        return self.__PROJECT_FILE_TEMPLATE.substitute(
            project_name=self.__project_name,
            project_references=project_references,
            natures=natures,
            links=links
        )

    def add_link(self, name, location, folder=False):
        if name.startswith(".."):
            raise ValueError('invalid name "' + name + '", a name can not start with dots')
        self.__links.append([name, location, folder, True])

    def add_project_reference(self, name):
        self.__project_references.append(name)

    def write(self, destination):
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

    def __str__(self):
        return "<project>={0}".format(self.version)

    def write_version(self, destination):
        settings_dir = os.path.join(destination, ".settings")
        # Create .settings dir if it doesn't yet exist
        if not os.path.exists(settings_dir):
            os.makedirs(settings_dir)
        version_file_path = "com.sigasi.hdt.{0}.version.prefs".format(self.lang)
        version_file = os.path.join(settings_dir, version_file_path)
        if self.version is not None and not os.path.exists(version_file):
            SettingsFileWriter.write(settings_dir, version_file_path, str(self))


class SigasiProjectCreator:
    """This class helps you to easily create a Sigasi project (".project")
    and library mapping (".library_mapping.xml") file.
    It will also create a .settings folder if it doesn't yet exist, see ProjectVersionCreator.

    Typical example:
        creator = SigasiProjectCreator(project_name, VhdlVersion.NINETY_THREE)
        creator.add_link("test.vhd", "/home/heeckhau/shared/test.vhd")
        creator.add_mapping("test.vhd", "myLib")
        creator.write("/home/heeckhau/test/")
    """

    def __init__(self, project_name, vhdl_version=VhdlVersion.NINETY_THREE, verilog_version=None):
        check_hdl_versions(vhdl_version, verilog_version)
        self.__libraryMappingFileCreator = LibraryMappingFileCreator(vhdl_version, verilog_version)
        self.__projectFileCreator = ProjectFileCreator(project_name, vhdl_version, verilog_version)
        self.__projectVersionCreators = []
        if vhdl_version:
            self.__projectVersionCreators.append(ProjectVersionCreator(vhdl_version))
        if verilog_version:
            self.__projectVersionCreators.append(ProjectVersionCreator(verilog_version))

    def add_link(self, name, location, folder=False):
        location = location.replace("\\", "/")
        self.__projectFileCreator.add_link(name, location, folder)

    def add_mapping(self, path, library):
        path = path.replace("\\", "/")
        self.__libraryMappingFileCreator.add_mapping(path, library)

    def unmap(self, path):
        path = path.replace("\\", "/")
        self.__libraryMappingFileCreator.unmap(path)

    def write(self, destination):
        self.__projectFileCreator.write(destination)
        self.__libraryMappingFileCreator.write(destination)
        for projectVersionCreator in self.__projectVersionCreators:
            projectVersionCreator.write(destination)

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
