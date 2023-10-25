import pathlib

from SigasiProjectCreator.ProjectOptions import ProjectOptions


def write(destination, name, content):
    settings_file = pathlib.Path(destination).joinpath(name)
    assert (ProjectOptions.get_force_overwrite() or not settings_file.exists()), f'*ERROR* project ' \
        f'file {settings_file} exists, won\'t overwrite (use `-f` or `--force` to overwrite)'
    with open(settings_file, "wb") as f:
        f.write(content.encode())
