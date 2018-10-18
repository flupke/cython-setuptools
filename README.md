# cython-setuptools
[![Build Status](https://travis-ci.org/flupke/cython-setuptools.svg?branch=master)](https://travis-ci.org/flupke/cython-setuptools)

Easier distribution and development of Cython modules.

Features:

* C/C++ files generated from Cython can be included in the VCS, or not
  (in which case they are generated on the fly from Cython files)
* Cython modules are defined in `setup.cfg`
* Cython can be specified in `install_requires`, `pip` properly installs it
  before compiling Cython modules

## Installation

```shell
$ pip install cython-setuptools
```

## Usage

```shell
$ cd your-python-project/
$ cython-setuptools install
```

Then use `cython-setuptools`' `setup()` in your `setup.py`:

```python
from cysetuptools import setup

setup()
```

And define your Cython modules in `setup.cfg`:

```ini
[cython-defaults]
include_dirs = include/

[cython-module: foo.bar]
sources = foo.pyx
          bar.cpp
include_dirs = eval(__import__('numpy').get_include())
language = c++
pkg_config_packages = opencv
```

Then your Cython modules can be compiled and tested in-place with:

```shell
$ python setup.py build_ext --inplace
```
