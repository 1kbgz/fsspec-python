from fsspec import filesystem

from fsspec_python.fs import PythonFileSystem


class TestFs:
    def test_fs_import(self, fs_importer):
        import my_local_file2

        assert my_local_file2.baz() == "This is a local file."

    def test_instance_needs_args(self):
        try:
            PythonFileSystem()
        except ValueError as e:
            assert str(e) == "Please provide filesystem instance(fs) or target_protocol"
        else:
            assert False, "Expected ValueError"

    def test_instance_needs_one_arg(self):
        try:
            PythonFileSystem(fs="something", target_protocol="file")
        except ValueError as e:
            assert str(e) == "Both filesystems (fs) and target_protocol may not be both given."
        else:
            assert False, "Expected ValueError"

        fs = PythonFileSystem(target_protocol="file", fo=".")
        assert fs.target_protocol == "file"
        assert fs.fs.protocol[0] == "file"
        fs.exit()

    def test_instance_with_fs(self):
        fs2 = filesystem("file")
        fs = PythonFileSystem(fs=fs2)
        assert fs.target_protocol == "file"
        assert fs.fs is fs2
        fs.exit()

    def test_instance_methods(self):
        fs2 = filesystem("file")
        fs = PythonFileSystem(fs=fs2)
        assert fs.fs is fs2
        assert fs._cached is True
        assert fs.listdir(".") == fs2.listdir(".")
        assert set(fs.__dict__.keys()) == {
            "__doc__",
            "__init__",
            "__module__",
            "_cache",
            "_isfilestore",
            "_latest",
            "_open",
            "_parent",
            "_pid",
            "_strip_protocol",
            "chmod",
            "cp_file",
            "created",
            "fsid",
            "get_file",
            "info",
            "isdir",
            "isfile",
            "islink",
            "lexists",
            "link",
            "local_file",
            "ls",
            "makedirs",
            "mkdir",
            "modified",
            "mv",
            "protocol",
            "put_file",
            "rm",
            "rm_file",
            "rmdir",
            "root_marker",
            "symlink",
            "touch",
            "unstrip_protocol",
        }
