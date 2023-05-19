import os


def get_version_number(root_folder):
    version = None
    with open(os.path.join(root_folder, "VERSION"), "r") as fp:
        version = fp.readlines(1)[0]

    return version
