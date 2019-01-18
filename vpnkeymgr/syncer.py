"""Terminal keys synchronizer."""

from subprocess import run

from vpnkeymgr.common import PKI


__all__ = ['Syncer']


HOST = 'srv.homeinfo.de'
PATH = '/usr/lib/terminals/keys'
USER = 'termgr'
CMD_TEMP = (
    '/usr/bin/rsync -auvce "/usr/bin/ssh {identity} '
    '-o UserKnownHostsFile=/dev/null '
    '-o StrictHostKeyChecking=no '
    '-o ConnectTimeout=5" '
    '--chmod=F640 '
    '{files} {user}@{host}:{path}')
KEYS_DIR = 'keys'


class Syncer(PKI):
    """Synchronizes OpenVPN keys."""

    def __init__(self, basedir, *clients):
        """Sets desired clients and an optional basedir."""
        super().__init__(basedir)
        self.clients = clients

    @property
    def files(self):
        """Yields client files."""
        yield self.pki_dir.joinpath('ca.crt')

        for client in self.clients:
            yield self.keys_dir.joinpath(f'{client}.key')
            yield self.keys_dir.joinpath(f'{client}.crt')

    def sync(self, host=None, path=None, user=None, identity=None):
        """Synchronizes the respective files to the specified destination
        with an optional alternative user and identity file.
        """
        cmd = CMD_TEMP.format(
            identity=f'-i {identity}' if identity else '',
            files=' '.join(str(file) for file in self.files),
            user=USER if user is None else user,
            host=HOST if host is None else host,
            path=PATH if path is None else path)
        return run(cmd, shell=True)
