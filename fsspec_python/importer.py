from __future__ import annotations

import sys
from importlib.abc import MetaPathFinder, SourceLoader
from importlib.machinery import SOURCE_SUFFIXES, ModuleSpec
from os.path import join
from types import ModuleType
from typing import TYPE_CHECKING, Dict, Union

from fsspec import url_to_fs
from fsspec.implementations.local import AbstractFileSystem

from .fs import PythonFileSystem
from .utils import normalize_fsspec

if TYPE_CHECKING:
    from collections.abc import Sequence


__all__ = (
    "FSSpecImportFinder",
    "FSSpecImportLoader",
    "install_importer",
    "uninstall_importer",
)


class FSSpecImportFinder(MetaPathFinder):
    def __init__(self, fs: PythonFileSystem) -> None:
        self.fs: PythonFileSystem = fs
        self.remote_modules: dict[str, str] = {}

    def find_spec(self, fullname: str, path: Sequence[str | bytes] | None, target: ModuleType | None = None) -> ModuleSpec | None:
        for suffix in SOURCE_SUFFIXES:
            filename = join(self.fs.root, fullname.split(".")[-1] + suffix)
            if not self.fs.exists(filename):
                continue
            self.remote_modules[fullname] = ModuleSpec(
                name=fullname, loader=FSSpecImportLoader(fullname, filename, self.fs), origin=filename, is_package=False
            )
            return self.remote_modules[fullname]
        return None

    def unload(self) -> None:
        # unimport all remote modules from sys.modules
        for mod in self.remote_modules:
            # TODO: what if imported by another?
            sys.modules.pop(mod, None)
        self.remote_modules = {}

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FSSpecImportFinder):
            return False
        return self.fs == other.fs


# Singleton for use elsewhere
_finders: Dict[str, FSSpecImportFinder] = {}


class FSSpecImportLoader(SourceLoader):
    def __init__(self, fullname: str, path: str, fs: PythonFileSystem):
        self.fullname = fullname
        self.path = path
        self.fs = fs

    def get_filename(self, fullname: str) -> str:  # noqa: ARG002
        return self.path

    def get_data(self, path: str | bytes) -> bytes:
        with self.fs.open(path, "rb") as f:
            return f.read()

    # def exec_module(self, module: ModuleType) -> None:
    #     source_bytes = self.get_data(self.get_filename(self.fullname))
    #     source = source_bytes.decode("utf-8")


def install_importer(fs: Union[str, AbstractFileSystem], **kwargs: str) -> FSSpecImportFinder:
    """Install the fsspec importer."""
    if isinstance(fs, AbstractFileSystem):
        fsspec_str = normalize_fsspec(fs=fs, **kwargs)
    elif not isinstance(fs, str):
        raise ValueError("fs must be a string or AbstractFileSystem instance")
    else:
        fsspec_str = fs
        assert "fo" not in kwargs, "fo cannot be used with string fs"
        fs, kwargs["fo"] = url_to_fs(fsspec_str)

    global _finders
    if fsspec_str not in _finders:
        python_fs = fs if isinstance(fs, PythonFileSystem) else PythonFileSystem(fs=fs, install=False, **kwargs)

        finder = FSSpecImportFinder(python_fs)
        _finders[fsspec_str] = finder
        sys.meta_path.insert(0, finder)
    return _finders[fsspec_str].fs


def uninstall_importer(fs: Union[str, AbstractFileSystem] = "") -> None:
    """Uninstall the fsspec importer."""
    global _finders
    if not _finders:
        return

    # clear last
    fs = list(_finders.keys())[-1] if not fs else fs
    fsspec_str = normalize_fsspec(fs=fs) if isinstance(fs, AbstractFileSystem) else fs

    if fsspec_str in _finders:
        finder = _finders.pop(fsspec_str, None)
        if finder:
            finder.unload()
        if finder in sys.meta_path:
            sys.meta_path.remove(finder)
        return
    raise ValueError(f"No importer found for {fsspec_str}")
