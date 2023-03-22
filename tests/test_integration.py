import os
import os.path as op
import shutil

import cython_setuptools


this_dir = op.dirname(__file__)
cython_setuptools_path = op.abspath(op.join(cython_setuptools.__file__, "..", ".."))


def _setup_source(setup_name, tmp_path):
    pypkg_dir = tmp_path / 'pypkg'
    src_dir = tmp_path / 'src'
    setup_path = pypkg_dir / 'setup.py'
    shutil.copytree(op.join(this_dir, 'pypkg'), str(pypkg_dir))
    shutil.copytree(op.join(this_dir, 'src'), str(src_dir))
    os.symlink(pypkg_dir / setup_name, setup_path)
    return setup_path, pypkg_dir


def test_compile_and_run_no_cythonize_mode(virtualenv, tmp_path):
    setup_path, pypkg_dir = _setup_source('setup-no-cythonize.py', tmp_path)
    virtualenv.run(f"pip install {cython_setuptools_path}")
    virtualenv.env.update({'CYTHONIZE': "1"})
    virtualenv.run(f"pip install -e {pypkg_dir}")
    assert virtualenv.run('python -m bar', capture=True) == '2\n'


def test_compile_and_run_cythonize_mode(virtualenv, tmp_path):
    setup_path, pypkg_dir = _setup_source('setup-cythonize.py', tmp_path)
    virtualenv.run(f"pip install {cython_setuptools_path}")
    virtualenv.run(f"pip install -e {pypkg_dir}")
    assert virtualenv.run('python -m bar', capture=True) == '2\n'
