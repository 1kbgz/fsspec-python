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
