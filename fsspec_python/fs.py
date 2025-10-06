from __future__ import annotations

import inspect

from fsspec import AbstractFileSystem, filesystem

from .importer import install_importer, uninstall_importer

__all__ = ("PythonFileSystem",)


class PythonFileSystem(AbstractFileSystem):
    """Python import filesystem"""

    def __init__(self, target_protocol=None, target_options=None, fs=None, **kwargs):
        """
        Args:
            target_protocol: str (optional) Target filesystem protocol. Provide either this or ``fs``.
            target_options: dict or None Passed to the instantiation of the FS, if fs is None.
            fs: filesystem instance The target filesystem to run against. Provide this or ``protocol``.
        """
        super().__init__(**kwargs)
        if fs is None and target_protocol is None:
            raise ValueError("Please provide filesystem instance(fs) or target_protocol")
        if not (fs is None) ^ (target_protocol is None):
            raise ValueError("Both filesystems (fs) and target_protocol may not be both given.")

        target_options = target_options or {}
        self.target_protocol = (
            target_protocol if isinstance(target_protocol, str) else (fs.protocol if isinstance(fs.protocol, str) else fs.protocol[0])
        )
        self.fs = fs if fs is not None else filesystem(target_protocol, **target_options)

        if target_protocol and kwargs.get("fo"):
            install_importer(f"{self.target_protocol}://{kwargs['fo']}", **target_options)
        else:
            install_importer(self.fs, **target_options, **kwargs)

    def close(self):
        uninstall_importer(self.target_protocol)
        self.fs.close()
        super().close()

    def __getattribute__(self, item):
        if item in {
            "__init__",
            "__getattribute__",
            "__reduce__",
            "_make_local_details",
            "open",
            "cat",
            "cat_file",
            "_cat_file",
            "cat_ranges",
            "_cat_ranges",
            "get",
            "read_block",
            "tail",
            "head",
            "info",
            "ls",
            "exists",
            "isfile",
            "isdir",
            "_check_file",
            "_check_cache",
            "_mkcache",
            "clear_cache",
            "clear_expired_cache",
            "pop_from_cache",
            "local_file",
            "_paths_from_path",
            "get_mapper",
            "open_many",
            "commit_many",
            "hash_name",
            "__hash__",
            "__eq__",
            "to_json",
            "to_dict",
            "cache_size",
            "pipe_file",
            "pipe",
            "start_transaction",
            "end_transaction",
        }:
            return object.__getattribute__(self, item)
        d = object.__getattribute__(self, "__dict__")
        fs = d.get("fs", None)  # fs is not immediately defined
        if item in d:
            return d[item]
        if fs is not None:
            if item in fs.__dict__:
                # attribute of instance
                return fs.__dict__[item]
            # attributed belonging to the target filesystem
            cls = type(fs)
            m = getattr(cls, item)
            if (inspect.isfunction(m) or inspect.isdatadescriptor(m)) and (not hasattr(m, "__self__") or m.__self__ is None):
                # instance method
                return m.__get__(fs, cls)
            return m  # class method or attribute
        # attributes of the superclass, while target is being set up
        return super().__getattribute__(item)
