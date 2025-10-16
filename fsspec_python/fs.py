from __future__ import annotations

import inspect

from fsspec import filesystem, register_implementation
from fsspec.implementations.chained import ChainedFileSystem

__all__ = ("PythonFileSystem",)


class PythonFileSystem(ChainedFileSystem):
    """Python import filesystem"""

    protocol: str = "python"
    root: str = "/"

    def __init__(self, target_protocol=None, target_options=None, fs=None, install: bool = True, **kwargs):
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
        self.root = kwargs.get("fo", "") or "/"

        if install:
            from .importer import install_importer

            install_importer(fs=self, **kwargs)

    def exit(self):
        from .importer import uninstall_importer

        uninstall_importer(self)
        if hasattr(self, "fs") and self.fs is not None and hasattr(self.fs, "exit"):
            self.fs.exit()

    def __getattribute__(self, item):
        if item in {
            "__doc__",
            "__init__",
            "__module__",
            "__new__",
            "exit",
            "fs",
            "protocol",
            "registered_name",
            "target_protocol",
        }:
            return object.__getattribute__(self, item)

        # Otherwise pull it out of dict
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


register_implementation(PythonFileSystem.protocol, PythonFileSystem)
