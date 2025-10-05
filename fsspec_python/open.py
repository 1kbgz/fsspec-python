import builtins

_original_open = builtins.open

__all__ = ("open_from_fsspec", "install_open_hook")


def open_from_fsspec(file, mode="r", buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None):
    print(f"Intercepted open call for: '{file}' with mode: '{mode}'")
    return _original_open(file, mode, buffering, encoding, errors, newline, closefd, opener)


def install_open_hook():
    builtins.open = open_from_fsspec
    globals()["open"] = open_from_fsspec
