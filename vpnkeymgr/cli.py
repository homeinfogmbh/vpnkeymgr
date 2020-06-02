"""Command line interface functions."""

from argparse import ArgumentParser
from pathlib import Path
from subprocess import CalledProcessError
from sys import stderr

from vpnkeymgr.config import CONFIG
from vpnkeymgr.exceptions import CommonNameExists
from vpnkeymgr.functions import print_cpr
from vpnkeymgr.generator import Keygen
from vpnkeymgr.syncer import Syncer


__all__ = ['main']


DESCRIPTION = 'OpenVPN key management utility.'


def generate(args):
    """Generates a new VPN key."""

    keygen = Keygen(args.basedir)

    try:
        key_name, completed_process = keygen.genkey(name=args.name)
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
    subparsers = parser.add_subparsers()
    gen = subparsers.add_parser('gen', help='generate certificates')
    gen.set_defaults(func=generate)
    sync = subparsers.add_parser('gen', help='generate certificates')
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
    sync.set_defaults(func=synchronize)
    return parser.parse_args()


def main():
    """Runs the VPN key manager."""

    args = get_args()
    return args.func(args)
