"""OpenVPN key generator."""

from subprocess import CalledProcessError, run
from sys import stderr
from uuid import uuid4

from vpnkeymgr.exceptions import CalledProcessErrors, CommonNameExists
from vpnkeymgr.functions import get_command
from vpnkeymgr.pki import PKI


__all__ = ['Keygen']


class Keygen(PKI):
    """OpenVPN key generator."""

    def exists(self, name):
        """Checks whether we already issued
        a certificate for this common name.
        """
        keyfile = self.keys_dir.joinpath(f'{name}.key')
        crtfile = self.certs_dir.joinpath(f'{name}.crt')
        return keyfile.exists() or crtfile.exists()

    def genkey(self, name=None):
        """Generates a new key."""
        name = uuid4().hex if name is None else name

        if self.exists(name):
            raise CommonNameExists(name)

        command = get_command(name)
        completed_process = run(command, cwd=self.basedir, check=True)
        return (name, completed_process)

    def genkeys(self, *names):
        """Generates multiple keys."""
        called_process_errors = []

        for name in names:
            try:
                name, completed_process = self.genkey(name=name)
            except CommonNameExists as common_name_exists:
                print(f'Common name "{common_name_exists}" already exists.',
                      file=stderr, flush=True)
                continue

            try:
                completed_process.check_returncode()
            except CalledProcessError as called_process_error:
                called_process_errors.append(called_process_error)
                continue

            yield name

        if called_process_errors:
            raise CalledProcessErrors(called_process_errors)
