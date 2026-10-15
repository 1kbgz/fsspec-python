# Python integration reference

Public names are exported from `fsspec_python` unless stated otherwise.

## Importers

### `install_importer(fs, **kwargs)`

Accepts a URL string or `AbstractFileSystem`. For an instance, `fo` supplies the
module root. A URL already supplies its root; passing `fo` with a string raises
`AssertionError`. Other input types raise `TypeError`.

Returns the installed `PythonFileSystem`. Repeated installation of the same normalized root reuses its importer.
New finders are inserted at the front of `sys.meta_path`.

### `uninstall_importer(fs="")`

Accepts the original URL or returned filesystem. An empty argument removes the
last installed importer. With no installed importers, it does nothing. An unknown
root raises `ValueError` when other importers remain installed.

Removal deletes the finder's tracked module names from `sys.modules` and removes
the finder from `sys.meta_path`. Existing references to module objects remain valid.

### `PythonFileSystem(target_protocol=None, target_options=None, fs=None, install=True, **kwargs)`

Chained filesystem with protocol `python`. Exactly one of `target_protocol` and
`fs` is required. `target_options` configures a newly constructed target; `fo` sets
the source root for an unchained target. `install=False` suppresses automatic
importer registration. `exit()` removes the importer and calls the target's
`exit()` when available.

### `FSSpecImportFinder` and `FSSpecImportLoader`

The finder checks the configured root for the final component of a module name
plus a Python source suffix. Matches have `is_package=False`. Package directories,
namespace packages, native extensions, and normal package-relative search are not
implemented. The loader reads source bytes with the filesystem's `open`.

## Open hook

### `install_open_hook(fsspec, **fsspec_args)`

Resolves a root URL with fsspec and replaces `builtins.open`. Read paths present on
the backend use that backend; missing read paths use the original builtin.
Modes containing `w`, `a`, or `x` always use the backend.

Backend calls receive `mode`, `encoding`, `errors`, and `newline`. `buffering`,
`closefd`, and `opener` are forwarded only on the local fallback path. Nested
installations do not form a restoration stack.

### `uninstall_open_hook()`

Restores the builtin saved when `fsspec_python.open` was imported.

## Other modules

`fsspec_python.utils.normalize_fsspec(fs=None, target_protocol=None, target_options=None, fo="", **kwargs)` returns a protocol/root string. Exactly
one of `fs` and `target_protocol` is required. The key does not include credentials
or storage options.

The `path` and `pathlib` modules contain no implemented hooks.
