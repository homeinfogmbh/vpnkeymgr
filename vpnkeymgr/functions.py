"""Common functions."""

from contextlib import suppress
from sys import stderr


__all__ = ['get_command', 'print_cpr']


EASYRSA = '/usr/bin/easyrsa'
COMMAND = 'build-client-full'
NOPASS = 'nopass'


def print_cpr(called_process_error, stdout=True):
    """Prints a CalledProcessError."""

    if stdout:
        with suppress(AttributeError, ValueError):
            print(called_process_error.stdout.decode())

    with suppress(AttributeError, ValueError):
        print(called_process_error.stderr.decode(), file=stderr)


def get_command(common_name):
    """Returns a command tuple for the respective common name."""

    return (EASYRSA, COMMAND, common_name, NOPASS)