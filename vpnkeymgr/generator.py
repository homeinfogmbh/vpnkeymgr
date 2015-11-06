"""OpenVPN key generator"""

from uuid import uuid4


class Keygen():
    """Key generator"""

    def __init__(self, vars_file):
        """Sets the easy-rsa vars file"""
        self._vars_file = vars_file

    @property
    def vars_file(self):
        """Returns the easy-rsa vars file"""
        return self._ca

    def generate(self, name=None):
        """Generates a new key"""
        name = str(uuid4()) if name is None else name
        # TODO: implement
