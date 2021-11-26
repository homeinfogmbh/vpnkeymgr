"""Common exceptions."""

from subprocess import CalledProcessError


__all__ = ['CalledProcessErrors', 'CommonNameExists']


class CalledProcessErrors(Exception):
    """Indicates that there were errors during several process calls."""

    def __init__(self, called_process_errors: list[CalledProcessError]):
        """Sets the CalledProcessErrors."""
        super().__init__(called_process_errors)
        self.called_process_errors = called_process_errors

    def __iter__(self):
        """Yields the CalledProcessErrors."""
        return iter(self.called_process_errors)


class CommonNameExists(Exception):
    """Indicates that the respective common name
    has already a key / certificate issued.
    """
