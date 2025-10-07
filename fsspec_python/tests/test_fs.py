class TestFs:
    # def test_fs(self, fs_importer):
    #     fs = fs_importer
    #     import my_local_file2

    #     assert my_local_file2.baz() == "This is a local file."

    #     fs.close()

    def test_fs_union(self, fs_union_importer):
        fs = fs_union_importer
        import my_local_file3
        import my_local_file4

        assert my_local_file3.foo3() == "This is local file."
        assert my_local_file4.foo4() == "This is local file."

        import masked
        assert masked.masked() == 4

        fs.close()
