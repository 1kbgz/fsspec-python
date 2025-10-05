from __future__ import annotations

import sys
from importlib.abc import MetaPathFinder, SourceLoader
from importlib.machinery import SOURCE_SUFFIXES, ModuleSpec
from os.path import join
from types import ModuleType
from typing import TYPE_CHECKING

from fsspec import url_to_fs
from fsspec.implementations.local import AbstractFileSystem

if TYPE_CHECKING:
    from collections.abc import Sequence


__all__ = (
    "FSSpecImportFinder",
    "FSSpecImportLoader",
    "install_importer",
    "uninstall_importer",
)


class FSSpecImportFinder(MetaPathFinder):
    def __init__(self, fsspec: str, **fsspec_args: str) -> None:
        self.fsspec_fs: AbstractFileSystem
        self.root: str
        self.fsspec_fs, self.root = url_to_fs(fsspec, **fsspec_args)
        self.remote_modules: dict[str, str] = {}

    def find_spec(self, fullname: str, path: Sequence[str | bytes] | None, target: ModuleType | None = None) -> ModuleSpec | None:
        for suffix in SOURCE_SUFFIXES:
            filename = join(self.root, fullname.split(".")[-1] + suffix)
            if not self.fsspec_fs.exists(filename):
                continue
            self.remote_modules[fullname] = ModuleSpec(
                name=fullname, loader=FSSpecImportLoader(fullname, filename, self.fsspec_fs), origin=filename, is_package=False
            )
            return self.remote_modules[fullname]
        return None

    def unload(self) -> None:
        # unimport all remote modules from sys.modules
        for mod in self.remote_modules:
            if mod in sys.modules:
                del sys.modules[mod]
        self.remote_modules = {}


# Singleton for use elsewhere
_finder: FSSpecImportFinder = None


class FSSpecImportLoader(SourceLoader):
    def __init__(self, fullname: str, path: str, fsspec_fs: AbstractFileSystem):
        self.fullname = fullname
        self.path = path
        self.fsspec_fs = fsspec_fs

    def get_filename(self, fullname: str) -> str:  # noqa: ARG002
        return self.path

    def get_data(self, path: str | bytes) -> bytes:
        with self.fsspec_fs.open(path, "rb") as f:
            return f.read()

    # def exec_module(self, module: ModuleType) -> None:
    #     source_bytes = self.get_data(self.get_filename(self.fullname))
    #     source = source_bytes.decode("utf-8")


def install_importer(fsspec: str, **fsspec_args: str) -> FSSpecImportFinder:
    """Install the fsspec importer.

    Args:
        fsspec: fsspec filesystem string
    Returns: The finder instance that was installed.
    """
    global _finder
    if _finder is None:
        _finder = FSSpecImportFinder(fsspec, **fsspec_args)

    sys.meta_path.insert(0, _finder)
    return _finder


def uninstall_importer() -> None:
    """Uninstall the fsspec importer."""
    global _finder
    if _finder is not None and _finder in sys.meta_path:
        _finder.unload()
        sys.meta_path.remove(_finder)
        _finder = None
