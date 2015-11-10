"""Terminal key packages synchronizer"""
from tempfile import TemporaryDirectory
from os.path import join
from os import getcwd

from .packager import ClientPackager
from subprocess import run, CalledProcessError


class Syncer():
    """Synchronizes OpenVPN configuration packages"""

    USER = 'termgr'
    IDENTITY = '~/.ssh/termgr'
    PATH = '/usr/lib/terminals/keys'

    def __init__(self, *clients, basedir=None):
        """Sets desired clients and an optional basedir"""
        self._clients = clients
        self._basedir = basedir or getcwd()

    def __call__(self, host, path=None, user=None, identity=None):
        """Synchronizes the respective files to the specified destination
        with an optional alternative user and identity file
        """
        path = path or self.PATH
        user = user or self.USER
        identity = identity or self.IDENTITY
        cmd_temp = '/usr/bin/rsync -auvc {arcname} {host}:{fname}'
        failures = []
        with TemporaryDirectory() as tmpdir:
            for client in self._clients:
                tarfile = '{0}.tar'.format(client)
                fname = join(path, tarfile)
                arcname = join(tmpdir, tarfile)
                packager = ClientPackager(self._basedir)
                with open(arcname, 'wb') as tar:
                    tar.write(packager(client))
                cmd = cmd_temp.format(arcname=arcname, host=host, fname=fname)
                completed_process = run(cmd, shell=True)
                try:
                    completed_process.check_returncode()
                except CalledProcessError:
                    failures.append(client)
        if failures:
            print('Could not synchronize:', failures)
            return False
        else:
            return True
