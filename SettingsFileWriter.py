import os


def write(destination, name, content):
    library_mapping_file = os.path.join(destination, name)
    f = open(library_mapping_file, 'w')
    try:
        f.write(content)
    finally:
        f.close()
