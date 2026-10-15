# fsspec-python

Import Python source modules from fsspec filesystems.

[![Build Status](https://github.com/1kbgz/fsspec-python/actions/workflows/build.yaml/badge.svg?branch=main&event=push)](https://github.com/1kbgz/fsspec-python/actions/workflows/build.yaml)
[![codecov](https://codecov.io/gh/1kbgz/fsspec-python/branch/main/graph/badge.svg)](https://codecov.io/gh/1kbgz/fsspec-python)
[![License](https://img.shields.io/github/license/1kbgz/fsspec-python)](https://github.com/1kbgz/fsspec-python)
[![PyPI](https://img.shields.io/pypi/v/fsspec-python.svg)](https://pypi.python.org/pypi/fsspec-python)

`fsspec-python` adds a filesystem-backed finder to Python's import machinery and
provides an optional hook for `builtins.open`. Importers read source files from a
configured root; imported code runs in the current Python process.

## Documentation

Start with [Import a module from memory](docs/tutorial.md), a complete local lesson
that needs no remote service.

For application work, [install and remove importers](docs/how-to-import.md) or
[redirect file access](docs/how-to-open.md). The [API reference](docs/reference.md)
covers signatures, return values, lookup order, and limits. Read
[How filesystem imports interact with Python](docs/explanation.md) for the design
and process-wide effects.
