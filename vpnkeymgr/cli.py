"""Command line interface functions."""

from pathlib import Path
from subprocess import CalledProcessError
from sys import stderr

from vpnkeymgr.exceptions import CommonNameExists
from vpnkeymgr.functions import print_cpr
from vpnkeymgr.generator import Keygen
from vpnkeymgr.syncer import Syncer


__all__ = ['generate', 'synchronize']


def _basedir(options):
    """Returns the respective base dir."""

    if options['--basedir']:
        return Path(options['--basedir'])

    return Path.cwd()


def generate(options):
    """Generates a new VPN key."""

    name = options['<name>']
    keygen = Keygen(_basedir(options))

    try:
        key_name, completed_process = keygen.genkey(name=name)
    except CommonNameExists as common_name_exists:
        print(f'Common name "{common_name_exists}" already exists.',
              file=stderr, flush=True)
        return 2

    try:
        completed_process.check_returncode()
    except CalledProcessError:
        print('Failed to generate key.', file=stderr)
        return 1

    print(f'Generated key "{key_name}".')
    return 0


def synchronize(options):
    """Synchronizes keys to a remote host."""

    syncer = Syncer(_basedir(options), *options['<names>'])
    completed_process = syncer.sync(
        host=options['--host'], path=options['--path'], user=options['--user'],
        identity=options['--identity'])

    try:
        completed_process.check_returncode()
    except CalledProcessError as called_process_error:
        print_cpr(called_process_error)
        return 3

    return 0
