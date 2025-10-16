from fsspec import AbstractFileSystem

__all__ = ("normalize_fsspec",)


def normalize_fsspec(
    fs: AbstractFileSystem = None,
    target_protocol: str = None,
    target_options: dict = None,
    fo: str = "",
    **kwargs,
):
    """Utility to normalize fsspec filesystem input"""

    # Only allow fs or target_protocol, not both or neither
    if (fs is None) == (target_protocol is None):
        raise ValueError("Please provide filesystem instance(fs) or target_protocol")

    target_options = target_options or {}

    if isinstance(fs, AbstractFileSystem):
        from .fs import PythonFileSystem

        while isinstance(fs, PythonFileSystem):
            if fs.fs is None:
                raise ValueError("PythonFileSystem instance must have fs set")
            fo = fs.root if fo == "" else fo
            fs = fs.fs

        # Reassemble fsspec and args
        if isinstance(fs.protocol, str):
            target_protocol = fs.protocol
        else:
            target_protocol = fs.protocol[0]

    return f"{target_protocol}://{fo}"
