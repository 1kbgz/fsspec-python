# fsspec-python

Native python integration for fsspec backends

[![Build Status](https://github.com/1kbgz/fsspec-python/actions/workflows/build.yaml/badge.svg?branch=main&event=push)](https://github.com/1kbgz/fsspec-python/actions/workflows/build.yaml)
[![codecov](https://codecov.io/gh/1kbgz/fsspec-python/branch/main/graph/badge.svg)](https://codecov.io/gh/1kbgz/fsspec-python)
[![License](https://img.shields.io/github/license/1kbgz/fsspec-python)](https://github.com/1kbgz/fsspec-python)
[![PyPI](https://img.shields.io/pypi/v/fsspec-python.svg)](https://pypi.python.org/pypi/fsspec-python)

## Overview

This library wraps an [fsspec filesystem](https://github.com/fsspec/filesystem_spec) so that files and folders inside it can be imported in Python.

```python
from fsspec import open

open(f"python::s3://my-python-bucket")

import my_bucket_lib  # s3://my-python-bucket/my_bucket_lib.py
```

## Usage

In addition to the `python::` [chained protocol](https://filesystem-spec.readthedocs.io/en/latest/features.html#url-chaining) url, this library exposes a handful of functions and monkey patches for connecting Python internal mechanisms to an `fsspec`-based filesystem.

- install_importer: install an
- `install_importer(fsspec: str, **fsspec_args: str)`: install an fsspec url/args as an importer
- `uninstall_importer(fsspec: str = "")`: uninstall an fsspec url, or if nothing provided remove the last-installed one
- `install_open_hook(fsspec: str, **fsspec_args)`: monkeypatch Python's `open` builtin to run off an `fsspec` filesystem
- `uninstall_open_hook()`: remove the monkeypatched `open`

Coming soon:

- Monkey patching for `os` / `os.path` / `pathlib`

> [!NOTE]
> This library was generated using [copier](https://copier.readthedocs.io/en/stable/) from the [Base Python Project Template repository](https://github.com/python-project-templates/base).
