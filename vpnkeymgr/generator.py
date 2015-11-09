"""OpenVPN key generator"""

from uuid import uuid4
from subprocess import run, CalledProcessError
from os.path import dirname, basename

__all__ = ['Keygen']


class Keygen():
    """OpenVPN key generator"""

    def __init__(self, vars_file):
        """Sets the easy-rsa vars file"""
        self._vars_file = vars_file

    def __call__(self, name=None):
        """Generates a new key"""
        name = str(uuid4()) if name is None else name
        basedir = dirname(self._vars_file)
        vars_ = basename(self._vars_file)
        cmd = ('cd {basedir}; source {vars}; '
               'build-key --batch {name}').format(
            basedir=basedir, vars=vars_, name=name)
        cp = run(cmd, shell=True)
        try:
            cp.check_returncode()
        except CalledProcessError:
            return False
        else:
            return name

    def __str__(self):
        """Returns the path to the vars file"""
        return self._vars

    def genkeys(self, count):
        """Generates multiple keys"""
        result = True
        for _ in range(0, count):
            reply = self()
            result = reply and result
        return result
