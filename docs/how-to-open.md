# How to redirect file access

Use the open hook when code calls `builtins.open` and needs a filesystem-backed
root. Install the backend required by the URL first.

```python
from fsspec_python import install_open_hook, uninstall_open_hook

install_open_hook("memory://open-demo")
try:
    with open("result.txt", "w") as output:
        output.write("complete\n")
    with open("result.txt") as source:
        print(source.read().strip())
finally:
    uninstall_open_hook()
```

The output is `complete`. Replace the memory URL with your target root, and pass
backend storage options as keyword arguments to `install_open_hook`.

Keep the hook's lifetime short and restore it in `finally`. It changes
`builtins.open` for the whole process. Missing read paths fall back to the original
local `open`; write, append, and exclusive-create paths use the configured backend.

See [API reference](reference.md) for argument handling and unsupported hooks.
