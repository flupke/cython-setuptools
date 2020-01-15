from six import StringIO

from cython_setuptools import vendor


def test_parse_all_module_opts():

    def dummy_pkg_config(pkg_names, command, env):
        assert pkg_names == ['dummy']
        if command == '--cflags':
            return '-Ifoo'
        elif command == '--libs':
            return '-L"/sp ace/bar" -lbaz'

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
tags = bar foo
''')
    parsed = vendor.parse_setup_cfg(fp, pkg_config=dummy_pkg_config)
    assert parsed == {
        'foo.bar': {
            'sources': ['foo.cpp', 'bar.cpp'],
            'libraries': ['foo', 'baz'],
            'include_dirs': [
                '/usr/include/bar',
                '/usr/include/foo',
                'foo'
            ],
            'library_dirs': ['/usr/lib/foo', '/sp ace/bar'],
            'extra_compile_args': ['-g'],
            'extra_link_args': ['-v'],
            'language': 'c++',
            'tags': 'bar foo',
        },
    }


def test_parse_defaults():
    fp = StringIO('''
[cython-defaults]
language = c++
include_dirs = base
tags = bazz

[cython-module: one]
include_dirs = one''')
    parsed = vendor.parse_setup_cfg(fp)
    assert parsed['one']['include_dirs'] == ['base', 'one']
    assert parsed['one']['language'] == 'c++'
    assert parsed['one']['tags'] == 'bazz'


def test_extract_args():
    args, rest = vendor.extract_args(
        '-Ifoo -I bar -L /bar --a=a --b b and --rest',
        ['-I', '-L', '--a', '--b']
    )
    assert args == {'I': ['foo', 'bar'], 'L': ['/bar'], 'a': ['a'], 'b': ['b']}
    assert rest == 'and --rest'


def test_extract_missing_args():
    args, rest = vendor.extract_args('-a a', ['-b'])
    assert args == {}
    assert rest == '-a a'
