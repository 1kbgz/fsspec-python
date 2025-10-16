import os

import pytest


class TestRemoteImport:
    @pytest.mark.skipif(not os.environ.get("FSSPEC_S3_ENDPOINT_URL"), reason="S3 not configured")
    def test_importer_s3(self, s3_importer):
        import my_remote_file

        assert my_remote_file.foo() == "This is a remote file."

    def test_importer_local(self, local_importer):
        import my_local_file

        assert my_local_file.bar() == "This is a local file."

    def test_importer_local_multi(self, local_importer_multi):
        import fsspec_python.importer

        assert len(fsspec_python.importer._finders) == 2
        import my_local_file
        import my_local_file2

        assert my_local_file.bar() == "This is a local file."
        assert my_local_file2.baz() == "This is a local file."
