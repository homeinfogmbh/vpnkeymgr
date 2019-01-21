"""Terminal keys synchronizer."""

from subprocess import run

from vpnkeymgr.config import CONFIG
from vpnkeymgr.pki import PKI


__all__ = ['Syncer']


CMD_TEMP = (
    '/usr/bin/rsync -auvce "/usr/bin/ssh {identity} '
    '-o UserKnownHostsFile=/dev/null '
    '-o StrictHostKeyChecking=no '
    '-o ConnectTimeout=5" '
    '--chmod=F640 '
    '{files} {user}@{host}:{path}')


class Syncer(PKI):
    """Synchronizes OpenVPN keys."""

    def __init__(self, basedir, *clients):
        """Sets desired clients and an optional basedir."""
        super().__init__(basedir)
        self.clients = clients

    @property
    def files(self):
        """Yields client files."""
        yield self.ca_cert

        for client in self.clients:
            yield self.keys_dir.joinpath(f'{client}.key')
            yield self.certs_dir.joinpath(f'{client}.crt')

    def sync(self, host=None, path=None, user=None, identity=None):
        """Synchronizes the respective files to the specified destination
        with an optional alternative user and identity file.
        """
        if host is None:
            host = CONFIG['sync']['host']

        if path is None:
            path = CONFIG['sync']['path']

        if user is None:
            user = CONFIG['sync']['user']

        cmd = CMD_TEMP.format(
            identity=f'-i {identity}' if identity else '',
            files=' '.join(str(file) for file in self.files),
            user=user, host=host, path=path)
        return run(cmd, shell=True)
