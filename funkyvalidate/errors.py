"""
Exceptions raised by funkyvalidate package.
"""

class FunkyValidateException(Exception):
    """Base Exception type for package."""
    pass


class ValidationError(TypeError, FunkyValidateException):
    """Used in validation."""
    pass


class ValueABCException(FunkyValidateException):
    """
    """
    pass


class ValueABCAssertionError(ValueABCException, AssertionError):
    pass
