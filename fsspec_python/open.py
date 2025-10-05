import builtins
from os.path import join

import fsspec.implementations.local
from fsspec import url_to_fs
from fsspec.implementations.local import AbstractFileSystem

__all__ = ("install_open_hook", "uninstall_open_hook")

_original_open = builtins.open

# Patch fsspec's local open to avoid recursion
fsspec.implementations.local.open = _original_open


def install_open_hook(fsspec: str, **fsspec_args):
    fsspec_fs: AbstractFileSystem
    root: str
    fsspec_fs, root = url_to_fs(fsspec, **fsspec_args)

    print(root)

    def open_from_fsspec(file, mode="r", buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None):
        filename = join(root, file)
        print(filename)

        if ("w" in mode or "a" in mode or "x" in mode) or fsspec_fs.exists(filename):
            return fsspec_fs.open(filename, mode=mode, encoding=encoding, errors=errors, newline=newline)
        return _original_open(file, mode, buffering, encoding, errors, newline, closefd, opener)

    builtins.open = open_from_fsspec
    globals()["open"] = open_from_fsspec


def uninstall_open_hook():
    builtins.open = _original_open
    globals()["open"] = _original_open
