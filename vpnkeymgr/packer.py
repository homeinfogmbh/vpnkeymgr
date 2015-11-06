"""OpenVPN key packager"""

from tempfile import TemporaryFile
from os import getcwd
from os.path import join

import tarfile


class ClientKeyPackager():
    """Packs client keys"""

    KEYFILE = '{0}.key'
    CRTFILE = '{0}.crt'
    CA_FILE = 'ca.crt'

    def __init__(self, basedir=None):
        """Sets the base directory"""
        self._basedir = basedir or getcwd()

    def __call__(self, client):
        """Packages the files for the specified client"""
        keyfile = self.KEYFILE.format(client)
        crtfile = self.CRTFILE.format(client)
        ca_file = self.CA_FILE
        with TemporaryFile(mode='w+b') as tmp:
            with tarfile.open(mode='w', fileobj=tmp) as tar:
                tar.add(join(self._basedir, keyfile), arcname=keyfile)
                tar.add(join(self._basedir, crtfile), arcname=crtfile)
                tar.add(join(self._basedir, ca_file), arcname=ca_file)
            tmp.seek(0)
            return tmp.read()
