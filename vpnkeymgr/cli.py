"""Command line interface functions."""

from argparse import ArgumentParser
from logging import DEBUG, INFO, basicConfig, getLogger
from pathlib import Path
from subprocess import CalledProcessError

from vpnkeymgr.config import CONFIG
from vpnkeymgr.exceptions import CalledProcessErrors
from vpnkeymgr.functions import print_cpr
from vpnkeymgr.generator import Keygen
from vpnkeymgr.syncer import Syncer


__all__ = ['main']


DESCRIPTION = 'OpenVPN key management utility.'
LOG_FORMAT = '[%(levelname)s] %(name)s: %(message)s'
LOGGER = getLogger('vpnkeymgr')


def generate(args):
    """Generates a new VPN key."""

    keygen = Keygen(args.basedir)

    try:
        for name in keygen.genkeys(args.name):
            LOGGER.info('Generated key "%s".', name)
    except CalledProcessErrors as called_process_errors:
        for called_process_error in called_process_errors:
            LOGGER.error('Called process error: %s', called_process_error)

        return 2

    return 0


def synchronize(args):
    """Synchronizes keys to a remote host."""

    syncer = Syncer(args.basedir, *args.name)
    completed_process = syncer.sync(
        host=args.host, path=args.path, user=args.user, identity=args.identity)

    try:
        completed_process.check_returncode()
    except CalledProcessError as called_process_error:
        print_cpr(called_process_error)
        return 3

    return 0


def get_args():
    """Parses the command line arguments."""

    parser = ArgumentParser(description=DESCRIPTION)
    parser.add_argument(
        '-d', '--basedir', type=Path, default=Path.cwd(),
        help='base directory path')
    parser.add_argument(
        '--debug', action='store_true', help='print debug messages')
    subparsers = parser.add_subparsers()
    gen = subparsers.add_parser('gen', help='generate certificates')
    gen.set_defaults(func=generate)
    gen.add_argument(
        'name', nargs='+', metavar='name',
        help='the certificates to generate')
    sync = subparsers.add_parser('sync', help='synchronize certificates')
    sync.add_argument(
        '-u', '--user', default=CONFIG['sync']['user'],
        help='the target user name')
    sync.add_argument(
        '-H', '--host', default=CONFIG['sync']['host'],
        help='the target host name')
    sync.add_argument(
        '-p', '--path', default=CONFIG['sync']['path'],
        help='the target directory path')
    sync.add_argument(
        '-i', '--identity', help='the identity file to use')
    sync.add_argument(
        'name', nargs='*', metavar='name',
        help='the certificates to synchronize')
    sync.set_defaults(func=synchronize)
    return parser.parse_args()


def main():
    """Runs the VPN key manager."""

    args = get_args()
    basicConfig(format=LOG_FORMAT, level=DEBUG if args.debug else INFO)

    try:
        return args.func(args)
    except AttributeError:
        return 0
