"""Terminal keys synchronizer."""

from pathlib import Path
from subprocess import CompletedProcess, run
from typing import Optional, Union

from vpnkeymgr.functions import get_rsync_cmd
from vpnkeymgr.pki import PKI


__all__ = ['Syncer']


class Syncer(PKI):
    """Synchronizes OpenVPN keys."""

    def __init__(self, basedir: Union[Path, str], *clients: str):
        """Sets desired clients and an optional basedir."""
        super().__init__(basedir)
        self.clients = clients

    @property
    def files(self):
        """Yields client files."""
        yield self.ca_cert

        if self.crl.is_file():
            yield self.crl

        for client in self.clients:
            yield self.keys_dir / f'{client}.key'
            yield self.certs_dir / f'{client}.crt'

    def sync(self, host: str, path: Union[Path, str], user: str,
             identity: Optional[Union[Path, str]] = None) -> CompletedProcess:
        """Synchronizes the respective files to the specified destination
        with an optional alternative user and identity file.
        """
        cmd = get_rsync_cmd(
            f'-i {identity}' if identity else '', self.files, user=user,
            host=host, path=path)
        return run(cmd, check=True)
