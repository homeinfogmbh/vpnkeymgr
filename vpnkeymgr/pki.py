"""Common library for the VPN key manager."""

from pathlib import Path
from typing import Union


__all__ = ['PKI']


class PKI:
    """Base class for PKI."""

    def __init__(self, basedir: Union[Path, str]):
        """Sets the base dir."""
        self.basedir = Path(basedir)

    @property
    def pki_dir(self):
        """Returns the PKI directory."""
        return self.basedir / 'pki'

    @property
    def ca_cert(self):
        """Returns the path to the CA certificate."""
        return self.pki_dir / 'ca.crt'

    @property
    def crl(self):
        """Returns the path of the certificate revocation list."""
        return self.pki_dir / 'crl.pem'

    @property
    def keys_dir(self):
        """Returns the keys directory."""
        return self.pki_dir / 'private'

    @property
    def certs_dir(self):
        """Returns the keys directory."""
        return self.pki_dir / 'issued'
