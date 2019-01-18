"""Common library for the VPN key manager."""

from contextlib import suppress
from pathlib import Path
from sys import stderr


__all__ = ['print_cpr', 'PKI']


def print_cpr(called_process_error, stdout=True):
    """Prints a CalledProcessError."""

    if stdout:
        with suppress(AttributeError, ValueError):
            print(called_process_error.stdout.decode())

    with suppress(AttributeError, ValueError):
        print(called_process_error.stderr.decode(), file=stderr)


class PKI:
    """Base class for PKI."""

    def __init__(self, basedir):
        """Sets the base dir."""
        self.basedir = Path(basedir)

    @property
    def pki_dir(self):
        """Returns the PKI directory."""
        return self.basedir.joinpath('pki')

    @property
    def keys_dir(self):
        """Returns the keys directory."""
        return self.pki_dir.joinpath('private')

    @property
    def certs_dir(self):
        """Returns the keys directory."""
        return self.pki_dir.joinpath('issued')
