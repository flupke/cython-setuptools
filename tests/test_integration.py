import os.path as op
import shutil

import pytest
import cython_setuptools


this_dir = op.dirname(__file__)
cython_setuptools_path = op.abspath(op.join(cython_setuptools.__file__, "..", ".."))


@pytest.mark.slow
def test_compile_and_run_no_cythonize_mode(virtualenv, tmp_dir):
    setup_path, pypkg_dir = _setup_source('setup-no-cythonize.py', tmp_dir)
    virtualenv.run(f"pip install {cython_setuptools_path}")
    virtualenv.run('CYTHONIZE=1 pip install -e %s' % pypkg_dir)
    assert virtualenv.run('python -m bar', capture=True) == '2\n'


@pytest.mark.slow
def test_compile_and_run_cythonize_mode(virtualenv, tmp_dir):
    setup_path, pypkg_dir = _setup_source('setup-cythonize.py', tmp_dir)
    virtualenv.run(f"pip install {cython_setuptools_path}")
    virtualenv.run('pip install -e %s' % pypkg_dir)
    assert virtualenv.run('python -m bar', capture=True) == '2\n'


def _setup_source(setup_name, tmp_dir):
    pypkg_dir = tmp_dir.join('pypkg')
    src_dir = tmp_dir.join('src')
    setup_path = pypkg_dir.join('setup.py')
    shutil.copytree(op.join(this_dir, 'pypkg'), str(pypkg_dir))
    shutil.copytree(op.join(this_dir, 'src'), str(src_dir))
    setup_path.mksymlinkto(pypkg_dir.join(setup_name))
    return setup_path, pypkg_dir
