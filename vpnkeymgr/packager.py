"""OpenVPN key packager"""

from tempfile import TemporaryFile, NamedTemporaryFile
from os.path import join, basename

import tarfile

__all__ = ['ClientPackager']


class ClientPackager():
    """Packs client keys"""

    KEYFILE = '{0}.key'
    CRTFILE = '{0}.crt'
    CA_FILE = 'ca.crt'
    CONFIG_FILE = 'terminals.conf'
    CFG_TEMP = '/usr/share/terminals/openvpn.conf.temp'

    def __init__(self, basedir):
        """Sets the base directory"""
        self._basedir = basedir

    def package(self, client):
        """Packages the files for the specified client"""
        keyfile = self.KEYFILE.format(client)
        crtfile = self.CRTFILE.format(client)

        if basename(self._basedir) == 'keys':
            keysdir = self._basedir
        else:
            keysdir = join(self._basedir, 'keys')

        # Read configuration template
        with open(self.CFG_TEMP, 'r') as cfg_tempf:
            cfg_temp = cfg_tempf.read()

        # Render configuration template
        config = cfg_temp.format(crtfile=crtfile, keyfile=keyfile)

        # Add files to temporary archive
        with TemporaryFile(mode='w+b') as tmp:
            with tarfile.open(mode='w', fileobj=tmp) as tar:
                tar.add(join(keysdir, keyfile), arcname=keyfile)
                tar.add(join(keysdir, crtfile), arcname=crtfile)
                tar.add(join(keysdir, self.CA_FILE),
                        arcname=self.CA_FILE)

                with NamedTemporaryFile(mode='w+') as cfg:
                    cfg.write(config)
                    cfg.seek(0)
                    tar.add(cfg.name, arcname=self.CONFIG_FILE)

            tmp.seek(0)
            return tmp.read()
