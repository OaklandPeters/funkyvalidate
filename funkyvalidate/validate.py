"""

This should be replaced when pyinterfaces.generics is more 
developed and stable.
"""
import collections
import abc
import six

__all__ = [
    'validate',
    'ValidationError',
    'type_check'
]





@six.add_metaclass(abc.ABCMeta)
class Validator(object):
    """Interface for objects implementing the __validate__ protocol."""
    __validate__ = abc.abstractmethod(lambda: NotImplemented)


def validate(value, category=None, name="object"):
    """
    Generic function for validation
    @type: value: Any
    @type: category: Optional[Validator, type]
    @type: name: Optional[str]
    @rtype: Any
    """
    if hasattr(category, '__validate__'):
        return category.__validate__(value)
    elif isinstance(category, type):
        return type_check(value, category, name)
    elif category is None:
        return value
    else:
        raise TypeError(
            _complaint(category, (Validator, type, None), "category")
        )

def type_check(value, category, name):
    if not isinstance(value, category):
        raise ValidationError(_complaint(value, category, name))
    return value

def _complaint(value, types, name):
    if not _non_string_sequence(types):
        types = [types]
    return str.format(
        "'{0}' should be type {1}, not {2}.",
        name, typenames(*types), type(value).__name__
    )

def typenames(*values):
    """
    @type: values: Sequence[Any]
    @rtype: str
    """
    return ", or ".join(_typenames(*values))

def _typenames(*values):
    """
    @type: values: Sequence[Any]
    @rtype: Iterator[str]
    """
    for value in values:
        if isinstance(value, type):
            yield value.__name__
        else:
            yield type(value).__name__

def _non_string_sequence(obj):
    return isinstance(obj, collections.Sequence) and not isinstance(obj, basestring)



