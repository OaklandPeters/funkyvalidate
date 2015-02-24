"""
ValueABC is intended to smooth over python2-3 compatibility, by providing
access to ValueMeta, through direct inheritance.

Basically, ValueABC bears the __metaclass__, so other classes don't have
to do so directly.
"""
from six import add_metaclass

from .valuemeta import ValueMeta

@add_metaclass(ValueMeta)
class ValueABC(object):
    """Bears ValueMeta, so it can more easily be added to classes
    in both Python 2 and Python 3.
    """
    pass
