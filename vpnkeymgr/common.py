"""Common library for the VPN key manager."""

from contextlib import suppress
from sys import stderr

__all__ = ['FILES', 'print_called_process_error']


FILES = ('{}.key', '{}.csr', '{}.crt')


def print_called_process_error(called_process_error, stdout=True):
    """Prints a CalledProcessError."""

    if stdout:
        with suppress(AttributeError, ValueError):
            print(called_process_error.stdout.decode())

    with suppress(AttributeError, ValueError):
        print(called_process_error.stderr.decode(), file=stderr)
