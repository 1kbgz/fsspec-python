# How to install and remove importers

Point an importer at a directory containing `.py` modules. Install the fsspec
backend required by the URL in the same environment.

## Use a URL

Pass the root URL to `install_importer`, and retain the returned filesystem for
cleanup:

```python
from fsspec_python import install_importer, uninstall_importer

importer = install_importer("s3://my-python-bucket/modules")
try:
    import reporting_helpers

    result = reporting_helpers.build_report()
finally:
    uninstall_importer(importer)
```

Configure backend credentials through fsspec before installing the importer.
Use an explicit filesystem instance when passing backend options directly:

```python
import fsspec

from fsspec_python import install_importer, uninstall_importer

fs = fsspec.filesystem("s3", profile="reports")
importer = install_importer(fs, fo="my-python-bucket/modules")
try:
    import reporting_helpers
finally:
    uninstall_importer(importer)
```

## Use a chained URL

Resolve `python::` with `url_to_fs`; call `exit()` when finished:

```python
from fsspec import url_to_fs

import fsspec_python

fs, _ = url_to_fs("python::file:///srv/python-modules")
try:
    import reporting_helpers
finally:
    fs.exit()
```

Use source modules from a trusted location: importing executes their code with
this process's permissions. See the [reference](reference.md) for supported module
layouts and cleanup behavior.
