"""
    :copyright: (c) 2008-2024 Sigasi
    :license: BSD, see LICENSE for more details.
"""
import pathlib

from SigasiProjectCreator import abort_if_false


def write(destination, name, content, force_overwrite):
    settings_file = pathlib.Path(destination).joinpath(name)
    abort_if_false((force_overwrite or not settings_file.exists()),
                   f'*ERROR* project file {settings_file} exists, ' \
                   'won\'t overwrite (use `-f` or `--force` to overwrite)')
    with open(settings_file, "wb") as f:
        f.write(content.encode())
