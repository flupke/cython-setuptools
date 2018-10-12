import os
import os.path as op
import sys
import shutil

import click


@click.group('cython-setuptools')
def main():
    """
    Cython setuptools integration.
    """


@click.command('install')
def install():
    """
    Install cython-setuptools.

    This command installs or updates the top-level module required to use
    cython-setuptools in Python packages.

    It must be run in the directory containing the setup.py file.
    """
    if 'setup.py' not in os.listdir('.'):
        click.secho('setup.py not found in the current directory', fg='red',
                    bold=True)
        sys.exit(1)

    # Copy vendored module and update MANIFEST.in
    this_dir = op.dirname(__file__)
    vendor_module = op.join(this_dir, 'vendor.py')
    shutil.copy(vendor_module, 'cysetuptools.py')
    manifest_line = 'include cysetuptools.py'
    manifest_file = 'MANIFEST.in'
    if op.exists(manifest_file):
        _append_if_not_exist('MANIFEST.in', manifest_line)
    else:
        with open(manifest_file, 'w') as fp:
            fp.write('%s\n' % manifest_line)

    click.secho('cython-setuptools has been installed:', fg='green')
    click.secho('')
    click.secho('  * the cysetuptools module has been copied to '
                'this directory', fg='green')
    click.secho('  * MANIFEST.in was updated to include it in source '
                'distributions', fg='green')
    click.secho('')
    click.secho('You can now use cython-setuptools in your setup.py:')
    click.secho('')
    click.secho('    from cysetuptools import setup')
    click.secho('')
    click.secho('    setup(...)')
    click.secho('')


def _append_if_not_exist(filename, line):
    with open(filename) as fp:
        for existing_line in fp:
            if existing_line.strip() == line.strip():
                return
    with open(filename, 'a') as fp:
        fp.write('%s\n' % line.strip())


main.add_command(install)
