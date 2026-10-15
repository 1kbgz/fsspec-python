# Import a module from memory

We will create a Python module in an in-memory filesystem, import it, and remove
its importer.

## Install

Use Python 3.10 or newer:

```console
python -m pip install fsspec-python
```

## Create a module

Create `import_demo.py`:

```python
import fsspec

from fsspec_python import install_importer, uninstall_importer

fs = fsspec.filesystem("memory")
fs.pipe_file("/import-demo/hello_remote.py", b'def greet():\n    return "Hello from memory"\n')
print(fs.ls("/import-demo", detail=False))
```

Run `python import_demo.py`. The listing contains `/import-demo/hello_remote.py`.

## Import and call the function

Append:

```python
importer = install_importer(fs, fo="/import-demo")
try:
    import hello_remote

    print(hello_remote.greet())
finally:
    uninstall_importer(importer)
```

Run the script again. Its final line is:

```text
Hello from memory
```

## Check cleanup

Append:

```python
import sys

print("hello_remote" in sys.modules)
```

Run the script. The final line is `False`: removing the importer also removed its
tracked module from Python's module cache.

See [How to install and remove importers](how-to-import.md) to use a filesystem URL.
