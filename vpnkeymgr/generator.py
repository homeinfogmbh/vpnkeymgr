"""OpenVPN key generator."""

from subprocess import CalledProcessError, run
from sys import stderr
from uuid import uuid4

from vpnkeymgr.common import PKI


__all__ = ['CalledProcessErrors', 'Keygen']


EASYRSA = '/usr/bin/easyrsa'
COMMAND = 'build-client-full'
NOPASS = 'nopass'


class CommonNameExists(Exception):
    """Indicates that the respective common name
    has already a key / certificate issued.
    """


class CalledProcessErrors(Exception):
    """Indicates that there were errors during several process calls."""

    def __init__(self, called_process_errors):
        """Sets the CalledProcessErrors."""
        super().__init__(called_process_errors)
        self.called_process_errors = called_process_errors

    def __iter__(self):
        """Yields the CalledProcessErrors."""
        for called_process_error in self.called_process_errors:
            yield called_process_error


def get_command(common_name):
    """Returns a command tuple for the respective common name."""

    return (EASYRSA, COMMAND, common_name, NOPASS)


class Keygen(PKI):
    """OpenVPN key generator."""

    def exists(self, name):
        """Checks whether we already issued
        a certificate for this common name.
        """
        keyfile = '{}.key'.format(name)
        keyfile = self.keys_dir.joinpath(keyfile)
        crtfile = '{}.crt'.format(name)
        crtfile = self.certs_dir.joinpath(crtfile)
        return keyfile.exists() or crtfile.exists()

    def genkey(self, name=None):
        """Generates a new key."""
        name = str(uuid4()) if name is None else name

        if self.exists(name):
            raise CommonNameExists(name)

        command = get_command(name)
        completed_process = run(command, cwd=self.basedir)
        return (name, completed_process)

    def genkeys(self, *names):
        """Generates multiple keys."""
        called_process_errors = []

        for name in names:
            try:
                name, completed_process = self.genkey(name=name)
            except CommonNameExists as common_name_exists:
                print('Common name "{}" already exists.'.format(
                    common_name_exists), file=stderr, flush=True)
            else:
                try:
                    completed_process.check_returncode()
                except CalledProcessError as called_process_error:
                    called_process_errors.append(called_process_error)
                else:
                    yield name

        if called_process_errors:
            raise CalledProcessErrors(called_process_errors)
