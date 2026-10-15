# How filesystem imports interact with Python

Python asks finders in `sys.meta_path` to locate modules that are not already in
`sys.modules`. An fsspec finder adds another source location without copying that
location into a local package installation.

## A filesystem root acts as a source directory

The finder looks for a source file under its configured root and lets Python's
source loader execute the bytes. Backend authentication and storage access remain
fsspec responsibilities. The importer handles module lookup and lifetime.

This fits directories of standalone source modules. It does not implement the
package search rules needed for package directories or namespace packages.

## Registration affects the process

New finders go before existing finders, so a newly installed root can supply a name
that would otherwise resolve elsewhere. Python's module cache still takes
precedence: installing another finder does not replace an already imported module.

Removing an importer removes tracked entries from the cache. Code that retained a
reference to a module or function can still call it. Cleanup therefore removes
future lookup paths; it does not undo code execution or its side effects.

## File access is independent of import lookup

The open hook redirects calls to `builtins.open`, while the finder redirects module
lookup. Either can be used independently. The open hook's fallback for missing read
paths lets existing local file reads continue, but writes go to the configured
backend. Both mechanisms affect the whole process, which makes explicit cleanup
part of their lifecycle.

See the [tutorial](tutorial.md) for a complete importer lifecycle and the
[reference](reference.md) for lookup limits.
