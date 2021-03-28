"""Common functions."""

from contextlib import suppress
from pathlib import Path
from subprocess import CalledProcessError
from sys import stderr
from typing import Iterable, Union


__all__ = ['get_easyrsa_cmd', 'get_rsync_cmd', 'print_cpr']


EASYRSA = '/usr/bin/easyrsa'
COMMAND = 'build-client-full'
NOPASS = 'nopass'


def print_cpr(called_process_error: CalledProcessError, stdout: bool = True):
    """Prints a CalledProcessError."""

    if stdout:
        with suppress(AttributeError, ValueError):
            print(called_process_error.stdout.decode())

    with suppress(AttributeError, ValueError):
        print(called_process_error.stderr.decode(), file=stderr)


def get_easyrsa_cmd(common_name: str) -> list[str]:
    """Returns a command tuple for the respective common name."""

    return [EASYRSA, COMMAND, common_name, NOPASS]


def get_ssh_cmd(identity: Union[Path, str]) -> list[str]:
    """Returns the command for SSH."""

    return [
        f'/usr/bin/ssh {identity}',
        '-o',
        'UserKnownHostsFile=/dev/null',
        '-o',
        'StrictHostKeyChecking=no '
        '-o ConnectTimeout=5'
    ]


def get_rsync_cmd(identity: Union[Path, str], files: Iterable[Path],
                  user: str, host: str, path: Path) -> list[str]:
    """Returns the command for rsync."""

    return ' '.join([
        '/usr/bin/rsync',
        '-auvce',
        '"' + ' '.join(get_ssh_cmd(identity)) + '"',
        '--chmod=F640',
        *(str(file) for file in files),
        f'{user}@{host}:{path}'
    ])
