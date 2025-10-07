import os
import sys
from pathlib import Path

import pytest
from fsspec import url_to_fs

from fsspec_python import PythonFileSystem, install_importer, install_open_hook, uninstall_importer, uninstall_open_hook


@pytest.fixture()
def s3_importer():
    # For coverage
    uninstall_importer()

    sys_meta_path_length = len(sys.meta_path)
    if not os.environ.get("FSSPEC_S3_ENDPOINT_URL"):
        pytest.skip("S3 not configured")
    fs = install_importer("s3://timkpaine-public/projects/fsspec-python")
    if len(sys.meta_path) != sys_meta_path_length + 1:
        # reset, some others get registered
        sys_meta_path_length = len(sys.meta_path) - 1
    assert len(sys.meta_path) == sys_meta_path_length + 1
    yield fs.fs
    uninstall_importer()
    assert len(sys.meta_path) == sys_meta_path_length


@pytest.fixture()
def local_importer():
    sys_meta_path_length = len(sys.meta_path)
    install_importer(f"file://{Path(__file__).parent}/local")
    yield
    uninstall_importer()
    assert len(sys.meta_path) == sys_meta_path_length


@pytest.fixture()
def local_importer_multi():
    sys_meta_path_length = len(sys.meta_path)
    install_importer(f"file://{Path(__file__).parent}/local")
    # install_importer(f"file://{Path(__file__).parent}/local2")
    pfs = PythonFileSystem(target_protocol="file", fo=f"{Path(__file__).parent}/local2")
    install_importer(pfs)
    yield
    uninstall_importer()
    uninstall_importer()
    assert len(sys.meta_path) == sys_meta_path_length


@pytest.fixture()
def open_hook():
    sys_meta_path_length = len(sys.meta_path)
    install_open_hook(f"file://{Path(__file__).parent}/dump/")
    yield
    uninstall_open_hook()
    assert len(sys.meta_path) == sys_meta_path_length


@pytest.fixture()
def fs_importer():
    sys_meta_path_length = len(sys.meta_path)
    fs, _ = url_to_fs(f"python::file://{Path(__file__).parent}/local2")
    yield fs
    fs.exit()
    assert len(sys.meta_path) == sys_meta_path_length
