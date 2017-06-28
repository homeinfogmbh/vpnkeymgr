"""Terminal keys synchronizer"""

from os.path import join
from subprocess import run

__all__ = ['Syncer']


class Syncer():
    """Synchronizes OpenVPN keys"""

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

    def __init__(self, basedir, *clients):
        """Sets desired clients and an optional basedir"""
        self.basedir = basedir
        self.clients = clients

    @property
    def keys_dir(self):
        """Returns the keys directory"""
        return join(self.basedir, self.KEYS_DIR)

    @property
    def files(self):
        """Yields client files"""
        yield 'ca.crt'

        for client in self.clients:
            yield '{}.key'.format(client)
            yield '{}.crt'.format(client)

    def sync(self, host=None, path=None, user=None, identity=None):
        """Synchronizes the respective files to the specified destination
        with an optional alternative user and identity file
        """
        host = host or self.HOST
        path = path or self.PATH
        user = user or self.USER
        files = ' '.join(join(self.keys_dir, f) for f in self.files)
        identity = self.IDENTITY.format(identity) if identity else ''
        cmd = self.CMD_TEMP.format(
            identity=identity, files=files, user=user, host=host, path=path)
        run(cmd, shell=True).check_returncode()
