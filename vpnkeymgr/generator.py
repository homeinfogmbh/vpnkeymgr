"""OpenVPN key generator"""

from uuid import uuid4
from subprocess import run, CalledProcessError

__all__ = ['Keygen']


class Keygen():
    """OpenVPN key generator"""

    def __init__(self, basedir, vars_file):
        """Sets the easy-rsa vars file"""
        self._basedir = basedir
        self._vars_file = vars_file

    def __str__(self):
        """Returns the path to the vars file"""
        return self._vars

    def genkey(self, name=None):
        """Generates a new key"""
        name = str(uuid4()) if name is None else name
        cmd = ('cd {basedir}; source {vars}; '
               './build-key --batch {name}').format(
            basedir=self._basedir, vars=self._vars_file, name=name)
        completed_process = run(cmd, shell=True)

        try:
            completed_process.check_returncode()
        except CalledProcessError:
            return False
        else:
            return name

    def genkeys(self, count):
        """Generates multiple keys"""
        result = True

        for _ in range(0, count):
            reply = self.genkey()
            result = reply and result

        return result
