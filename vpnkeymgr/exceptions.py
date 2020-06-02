"""Common exceptions."""


__all__ = ['CalledProcessErrors', 'CommonNameExists']


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


class CommonNameExists(Exception):
    """Indicates that the respective common name
    has already a key / certificate issued.
    """