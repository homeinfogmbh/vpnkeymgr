"""OpenVPN key generator"""

from uuid import uuid4
from subprocess import run

__all__ = ['Keygen']


class Keygen():
    """OpenVPN key generator"""

    GEN_CMD_TEMP = 'cd {basedir}; source {vars}; ./build-key --batch {name}'

    def __init__(self, basedir, vars_file):
        """Sets the easy-rsa vars file"""
        self.basedir = basedir
        self.vars_file = vars_file

    def __str__(self):
        """Returns the path to the vars file"""
        return self._vars

    def genkey(self, name=None):
        """Generates a new key"""
        name = str(uuid4()) if name is None else name
        cmd = self.GEN_CMD_TEMP.format(
            basedir=self.basedir, vars=self.vars_file, name=name)
        run(cmd, shell=True).check_returncode()
        return name
