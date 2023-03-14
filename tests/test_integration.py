from pathlib import Path
import platform
import shutil

import pytest

import cython_setuptools

this_dir = Path(__file__).parent
cython_setuptools_path = (Path(cython_setuptools.__file__).parent).parent


def _setup_source(setup_name, tmp_dir: Path):
    pypkg_dir = tmp_dir / "pypkg"
    src_dir = tmp_dir / "src"
    setup_path = pypkg_dir / "setup.py"
    shutil.copytree(this_dir / "pypkg", str(pypkg_dir))
    shutil.copytree(this_dir / "src", str(src_dir))
    setup_path.symlink_to(pypkg_dir / setup_name)
    return setup_path, pypkg_dir


@pytest.mark.skipif(
    platform.system().lower() == "windows",
    reason="Windows environment variable are not easy to manage",
)
def test_compile_and_run_external_cythonize_mode(virtualenv, tmp_dir):
    _, pypkg_dir = _setup_source("setup-no-cythonize.py", tmp_dir)
    virtualenv.run(f"pip install {cython_setuptools_path}")
    virtualenv.run(f"export CYTHONIZE=1; pip install -e {pypkg_dir.resolve()}")
    assert int(virtualenv.run("python -m bar", capture=True)) == 2


def test_compile_and_run_cythonize_mode(virtualenv, tmp_dir):
    _, pypkg_dir = _setup_source("setup-cythonize.py", tmp_dir)
    virtualenv.run(f"pip install {cython_setuptools_path}")
    virtualenv.run(f"pip install -e {pypkg_dir.resolve()}")
    assert int(virtualenv.run("python -m bar", capture=True)) == 2
