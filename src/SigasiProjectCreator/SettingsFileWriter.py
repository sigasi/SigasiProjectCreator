import pathlib


def write(destination, name, content, force_overwrite):
    settings_file = pathlib.Path(destination).joinpath(name)
    assert (force_overwrite or not settings_file.exists()), f'*ERROR* project ' \
        f'file {settings_file} exists, won\'t overwrite (use `-f` or `--force` to overwrite)'
    with open(settings_file, "wb") as f:
        f.write(content.encode())
