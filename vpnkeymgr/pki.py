"""Common library for the VPN key manager."""

from pathlib import Path


__all__ = ['PKI']


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
    def ca_cert(self):
        """Returns the path to the CA certificate."""
        return self.pki_dir.joinpath('ca.crt')

    @property
    def crl(self):
        """Returns the path of the certificate revocation list."""
        self.pki_dir.joinpath('crl.pem')

    @property
    def keys_dir(self):
        """Returns the keys directory."""
        return self.pki_dir.joinpath('private')

    @property
    def certs_dir(self):
        """Returns the keys directory."""
        return self.pki_dir.joinpath('issued')
