import os


def expand_path(path):
    return os.path.expanduser(path) if isinstance(path, str) and '~' == path[0] else path


def path_to_folder(path):
    """Finds the right-most forward-slash and returns all characters to the right of it"""
    return str(path[path.rfind("/") + 1:])


def filetype(path, with_period=False):
    """Finds the right-most period and returns all characters to the right of it"""
    if with_period:
        return os.path.splitext(path)[1]
    else:
        return os.path.splitext(path)[1][1:]
