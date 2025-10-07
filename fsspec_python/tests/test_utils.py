from fsspec_python.utils import normalize_fsspec


class TestUtils:
    def test_normalize_fsspec(self, s3_importer):
        assert normalize_fsspec(target_protocol="s3", fo="mybucket") == "s3://mybucket"
        assert normalize_fsspec(target_protocol="s3") == "s3://"
        assert normalize_fsspec(fs=s3_importer, fo="test") == "s3://test"
