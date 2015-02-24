"""
Convenience class for common use-case for __instancecheck__; namely,
simple type-checking based on whether abstract-methods have been implemented.
"""
import six

from . import valuemeta
from ..ducktype import meets

@six.add_metaclass(valuemeta.ValueMeta)
class InterfaceType(object):
    """
    Provides simple checking based on list of abstractmethods.
    """
    #__metaclass__ = valuemeta.ValueMeta
    @classmethod
    def __instancecheck__(cls, instance):
        return meets(instance, cls)
    @classmethod
    def __subclasscheck__(cls, subclass):
        return meets(subclass, cls)

