import os
from pathlib import Path

import pytest
from fsspec import open

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


@pytest.fixture()
def open_hook():
    from fsspec_python import install_open_hook, uninstall_open_hook

    install_open_hook(f"file://{Path(__file__).parent}/dump/")
    yield
    uninstall_open_hook()


@pytest.fixture()
def fs_importer():
    fs = open(f"python::file://{Path(__file__).parent}/local2")
    yield fs
    fs.close()

@pytest.fixture()
def fs_union_importer():
    fs = open(f"python::file://{Path(__file__).parent}/local3::python::file://{Path(__file__).parent}/local4")
    yield fs
    fs.close()
