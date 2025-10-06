class TestFs:
    def test_fs(self, fs_importer):
        fs = fs_importer
        import my_local_file2

        assert my_local_file2.baz() == "This is a local file."

        fs.close()
