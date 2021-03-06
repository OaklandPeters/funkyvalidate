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
    'type_check',
    'is_valid'
]


class ValidationError(TypeError):
    """Used in validation."""
    pass


@six.add_metaclass(abc.ABCMeta)
class Validator(object):
    """Interface for objects implementing the __validate__ protocol."""
    __validate__ = abc.abstractmethod(lambda: NotImplemented)


def validate(value, category=None, name="object", inner=None):
    """
    Generic function for validation. If an `inner` set of types is provided,
    will validate each element of `value` against them.
    @type: value: Any
    @type: category: Optional[Validator, type]
    @type: name: Optional[str]
    @type: inner: Optional[Validator, type]
    @rtype: Any
    """
    if category is not None:
        result = _validate(value, category=category, name=name)

    if inner is not None:
        _validate_inner(value, category=inner, name="object")

    return result


def _validate(value, category=None, name="object"):
    """
    Generic function for validation. If an `inner` set of types is provided,
    will validate each element of `value` against them.
    @type: value: Any
    @type: category: Optional[Validator, type]
    @type: name: Optional[str]
    @rtype: Any
    """
    if hasattr(category, 'validate'):
        return category.__validate__(value)
    elif isinstance(category, type):
        return type_check(value, category, name)
    elif category is None:  # Should this be here?
        return value
    elif isinstance(category, tuple):
        # A tuple of types. Ex. isinstance(myvar, (NoneType, str))
        for i, elm in enumerate(category):
            validate(elm, type, name="{0}[{1}]".format(name, i))
        return type_check(value, category, name)
    else:
        raise TypeError(
            _complaint(category, (Validator, type, None), "category")
        )

def _validate_inner(value, category=None, name="object"):
    """
    Exhausts an iterator, if inner is checked on an iterator.
    @type: value: Any
    @type: category: Optional[Validator, type]
    @type: name: str
    @rtype: None
    """
    validate(value, collections.Iterable)
    if not isinstance(value, collections.Iterable):
        raise TypeError(str.format(
            "validate_inner exhausts iterators. Collect into a Sequence before calling."
        ))

    for i, elm in enumerate(value):
        validate(elm, category, name="{0}[{1}]".format(name, i))

def is_valid(value, category=None, inner=None):
    try:
        validate(value, category=category, name="value", inner=inner)
    except ValidationError:
        return False
    return True


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

