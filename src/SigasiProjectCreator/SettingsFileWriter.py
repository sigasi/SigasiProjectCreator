import os

from SigasiProjectCreator.ArgsAndFileParser import ArgsAndFileParser


def write(destination, name, content):
    settings_file = os.path.abspath(os.path.join(destination, name))
    assert (ArgsAndFileParser.get_force_overwrite() or not os.path.exists(settings_file)), f'*ERROR* project ' \
        f'file {os.path.join(destination, name)} exists, won\'t overwrite (use `-f` or `--force` to overwrite)'
    with open(settings_file, "wb") as f:
        f.write(content.encode())
