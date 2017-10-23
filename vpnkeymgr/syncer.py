"""Terminal keys synchronizer."""

from subprocess import run

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
            yield f'{client}.key'
            yield f'{client}.crt'

    @property
    def paths(self):
        """Yields file paths."""
        for file in self.files:
            yield self.keys_dir.joinpath(file)

    def sync(self, host=None, path=None, user=None, identity=None):
        """Synchronizes the respective files to the specified destination
        with an optional alternative user and identity file.
        """
        cmd = self.command.format(
            identity=f'-i {identity}' if identity else '',
            files=' '.join(str(path) for path in self.paths),
            user=USER if user is None else user,
            host=HOST if host is None else host,
            path=PATH if path is None else path)
        return run(cmd, shell=True)
