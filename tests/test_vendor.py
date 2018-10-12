from StringIO import StringIO

from cython_setuptools import vendor


def test_parse_all_module_opts():

    def dummy_pkg_config(pkg_names):
        assert pkg_names == ['dummy']
        return '-Ipkg-config-include-dir -Lpkg-config-lib-dir -lpkg-config-lib'

    fp = StringIO('''
[cython-module: foo.bar]
sources = foo.cpp
          bar.cpp
libraries = foo
include_dirs = eval("/usr/include/bar")
               /usr/include/foo
library_dirs = /usr/lib/foo
extra_compile_args = -g
extra_link_args = -v
language = c++
pkg_config_packages = dummy
pkg_config_libraries = bar
''')
    parsed = vendor.parse_setup_cfg(fp, pkg_config=dummy_pkg_config)
    assert parsed == {
        'foo.bar': {
            'sources': ['foo.cpp', 'bar.cpp'],
            'libraries': ['foo', 'pkg-config-lib'],
            'include_dirs': [
                '/usr/include/bar',
                '/usr/include/foo',
                'pkg-config-include-dir',
            ],
            'library_dirs': ['/usr/lib/foo', 'pkg-config-lib-dir'],
            'extra_compile_args': ['-g'],
            'extra_link_args': ['-v'],
            'language': 'c++',
        },
    }


def test_parse_defaults():
    fp = StringIO('''
[cython-defaults]
language = c++
include_dirs = base

[cython-module: one]
include_dirs = one''')
    parsed = vendor.parse_setup_cfg(fp)
    assert parsed['one']['include_dirs'] == ['base', 'one']
    assert parsed['one']['language'] == 'c++'
