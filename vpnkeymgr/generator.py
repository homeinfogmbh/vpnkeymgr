"""OpenVPN key generator."""

from subprocess import CalledProcessError, run
from sys import stderr
from uuid import uuid4

from vpnkeymgr.common import FILES

__all__ = ['CalledProcessErrors', 'Keygen']


GEN_CMD_TEMP = 'cd {}; source {}; ./build-key --batch {}'


class CommonNameExists(Exception):
    """Indicates that the respective common name
    has already a key / certificate issued.
    """

    pass


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


class Keygen:
    """OpenVPN key generator."""

    def __init__(self, basedir, vars_file, command=GEN_CMD_TEMP):
        """Sets the easy-rsa vars file."""
        self.basedir = basedir
        self.vars_file = vars_file
        self.command = command

    def exists(self, name):
        """Checks whether we already issued
        a certificate for this common name.
        """
        for template in FILES:
            file = template.format(name)
            path = self.basedir.joinpath(file)

            if path.exists():
                return True

        return False

    def genkey(self, name=None):
        """Generates a new key."""
        name = str(uuid4()) if name is None else name

        if self.exists(name):
            raise CommonNameExists(name)

        cmd = self.command.format(self.basedir, self.vars_file, name)
        completed_process = run(cmd, shell=True)
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
