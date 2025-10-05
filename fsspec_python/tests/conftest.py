import os
from pathlib import Path

import pytest

from fsspec_python import install_importer, uninstall_importer


@pytest.fixture()
def s3_importer():
    if not os.environ.get("FSSPEC_S3_ENDPOINT_URL"):
        pytest.skip("S3 not configured")
    install_importer("s3://timkpaine-public/projects/fsspec-python")
    yield
    uninstall_importer()


@pytest.fixture()
def local_importer():
    install_importer(f"file://{Path(__file__).parent}/local")
    yield
    uninstall_importer()
