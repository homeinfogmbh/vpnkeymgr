"""OpenVPN key generator."""

from logging import getLogger
from subprocess import CalledProcessError, CompletedProcess, run
from typing import Iterator, NamedTuple, Optional
from uuid import uuid4

from vpnkeymgr.exceptions import CalledProcessErrors, CommonNameExists
from vpnkeymgr.functions import get_command
from vpnkeymgr.pki import PKI


__all__ = ['Keygen']


LOGGER = getLogger('vpnkeymgr')


class KeygenResult(NamedTuple):
    """Result from generating a key."""

    name: str
    completed_process: CompletedProcess


class Keygen(PKI):
    """OpenVPN key generator."""

    def exists(self, name: str) -> bool:
        """Checks whether we already issued
        a certificate for this common name.
        """
        keyfile = self.keys_dir.joinpath(f'{name}.key')
        crtfile = self.certs_dir.joinpath(f'{name}.crt')
        return keyfile.exists() or crtfile.exists()

    def genkey(self, name: Optional[str] = None) -> KeygenResult:
        """Generates a new key."""
        name = uuid4().hex if name is None else name

        if self.exists(name):
            raise CommonNameExists(name)

        command = get_command(name)
        completed_process = run(command, cwd=self.basedir, check=True)
        return KeygenResult(name, completed_process)

    def genkeys(self, *names: str) -> Iterator[str]:
        """Generates multiple keys."""
        called_process_errors = []

        for name in names:
            try:
                name, completed_process = self.genkey(name=name)
            except CommonNameExists:
                LOGGER.error('Common name "%s" already exists.', name)
                continue

            try:
                completed_process.check_returncode()
            except CalledProcessError as called_process_error:
                called_process_errors.append(called_process_error)
                continue

            yield name

        if called_process_errors:
            raise CalledProcessErrors(called_process_errors)
