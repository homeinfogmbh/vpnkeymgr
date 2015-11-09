"""OpenVPN key generator"""

from uuid import uuid4
from subprocess import run, CalledProcessError
from os.path import dirname, basename


class Keygen():
    """OpenVPN key generator"""

    def __init__(self, vars_file):
        """Sets the easy-rsa vars file"""
        self._vars_file = vars_file

    @property
    def vars_file(self):
        """Returns the easy-rsa vars file"""
        return self._vars_file

    def genkey(self, name):
        """Generates a new key"""
        basedir = dirname(self.vars_file)
        vars_ = basename(self.vars_file)
        cmd = ('cd {basedir}; source {vars}; '
               'build-key --batch {name}').format(
            basedir=basedir, vars=vars_, name=name)
        cp = run(cmd)
        try:
            cp.check_returncode()
        except CalledProcessError:
            return False
        else:
            return True

    def genkeys(self, count):
        """Generates multiple keys"""
        result = True
        for _ in range(0, count):
            name = str(uuid4())
            reply = self.genkey(name)
            result = reply and result
        return result
