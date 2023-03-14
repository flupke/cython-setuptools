# cython-setuptools
[![Build Status](https://travis-ci.org/flupke/cython-setuptools.svg?branch=master)](https://travis-ci.org/flupke/cython-setuptools)

Easier distribution and development of Cython modules.

Features:

* Two distribution models: with C/C++ files included in the package, and
  without
* Cython modules are defined in `setup.cfg`
* Install directly from Cython sources, without installing Cython in the target
  environment (Cython is only included in `install_requires`)

## Installation

```shell
$ pip install cython-setuptools
```

## Usage

Here is an example Python package using the default distribution model (only
Cython files are included in the source package).

First install the `cython-setuptools` vendor module in the package, next to
`setup.py`.

```shell
$ cd your-python-project/
$ cython-setuptools install
```

Then use `cython-setuptools`' `setup()` in your `setup.py`:

```python
from cysetuptools import setup

setup()
```

Note that we keep the default `cythonize=True` argument of `setup()` here,
meaning that C files are compiled from Cython files automatically.
`setup(cythonize=False)` would mean we would need to distribute the C/C++ files
compiled from Cython in the source package.

Define your Cython modules in `setup.cfg`.

```ini
[metadata]
name = your-python-project
version = 1.0

[options]
packages = find:
install_requires = cython

[options.extras_require]
dev = cython

[cython-defaults]
include_dirs = include/

[cython-module: foo.bar]
sources = foo.pyx
          bar.cpp
include_dirs = eval(__import__('numpy').get_include())
language = c++
cpp_std = 11
pkg_config_packages = opencv
```

Then your Cython modules can be compiled and tested in-place with:

```shell
$ python setup.py build_ext --inplace
```

This automatically compile outdated Cython files. If `setup(cythonize=False)`
is used, you have to specifically tell the setup to recompile outdated Cython
files:

```shell
$ CYTHONIZE=1 python setup.py build_ext --inplace
```
