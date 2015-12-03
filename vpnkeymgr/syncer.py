"""Terminal key packages synchronizer"""

from subprocess import run, CalledProcessError
from tempfile import TemporaryDirectory
from os.path import join
from sys import stderr

from .packager import ClientPackager

__all__ = ['Syncer']


class Syncer():
    """Synchronizes OpenVPN configuration packages"""

    HOST = 'srv.homeinfo.de'
    PATH = '/usr/lib/terminals/keys'
    USER = 'termgr'
    RSH = '-e "/usr/bin/ssh -i {identity}"'
    CMD = (
        '/usr/bin/rsync -auvc {rsh} '
        '-o UserKnownHostsFile=/dev/null '
        '-o StrictHostKeyChecking=no '
        '-o ConnectTimeout=5" '
        '--chmod=F640 '
        '{files} {user}@{host}:{path}'
    )

    def __init__(self, basedir, *clients):
        """Sets desired clients and an optional basedir"""
        self._basedir = basedir
        self._clients = clients

    def __call__(self, host=None, path=None, user=None, identity=None):
        """Synchronizes the respective files to the specified destination
        with an optional alternative user and identity file
        """
        host = host or self.HOST
        path = path or self.PATH
        user = user or self.USER
        rsh = self.RSH.format(identity) if identity else ''
        files = []
        failures = []
        with TemporaryDirectory() as tmpdir:
            for client in self._clients:
                tarfile = '{0}.tar'.format(client)
                arcname = join(tmpdir, tarfile)
                files.append(arcname)
                packager = ClientPackager(self._basedir)
                with open(arcname, 'wb') as tar:
                    tar.write(packager(client))
            files_ = ' '.join(files)
            cmd = self.CMD.format(
                rsh=rsh, files=files_, user=user, host=host, path=path
            )
            completed_process = run(cmd, shell=True)
            try:
                completed_process.check_returncode()
            except CalledProcessError:
                failures.append(client)
        if failures:
            print('Could not synchronize:', failures, file=stderr)
            return False
        else:
            return True
