"""Terminal keys synchronizer."""

from subprocess import run

__all__ = ['Syncer']


HOST = 'srv.homeinfo.de'
PATH = '/usr/lib/terminals/keys'
USER = 'termgr'
IDENTITY = '-i {}'
CMD_TEMP = (
    '/usr/bin/rsync -auvce "/usr/bin/ssh {identity} '
    '-o UserKnownHostsFile=/dev/null '
    '-o StrictHostKeyChecking=no '
    '-o ConnectTimeout=5" '
    '--chmod=F640 '
    '{files} {user}@{host}:{path}')
KEYS_DIR = 'keys'


class Syncer:
    """Synchronizes OpenVPN keys."""

    def __init__(self, basedir, *clients, command=CMD_TEMP, keys_dir=KEYS_DIR):
        """Sets desired clients and an optional basedir."""
        self.basedir = basedir
        self.clients = clients
        self.command = command
        self._keys_dir = keys_dir

    @property
    def keys_dir(self):
        """Returns the keys directory."""
        return self.basedir.joinpath(self._keys_dir)

    @property
    def files(self):
        """Yields client files."""
        yield 'ca.crt'

        for client in self.clients:
            yield '{}.key'.format(client)
            yield '{}.crt'.format(client)

    @property
    def paths(self):
        """Yields file paths."""
        for file in self.files:
            yield self.keys_dir.joinpath(file)

    def sync(self, host=HOST, path=PATH, user=USER, identity=None):
        """Synchronizes the respective files to the specified destination
        with an optional alternative user and identity file.
        """
        cmd = self.command.format(
            identity=IDENTITY.format(identity) if identity else '',
            files=' '.join(self.paths), user=user, host=host, path=path)
        return run(cmd, shell=True)
