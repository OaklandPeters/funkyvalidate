"""
Single file version.

"""

import collections
import abc
import six

# ===================================
# errors.py
# ===================================
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

 
# ===================================
# validate.py
# ===================================
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



# ===================================
# meets.py
# ===================================
def meets(obj, interface):
    """
    @type: obj: object
    @type: interface: abc.ABCMeta
    @rtype: bool
    """
    return not bool(list(missing_abstracts(obj, interface)))

def missing_abstracts(obj, interface):
    """
    __abstractmethods__ is generally only set on classes subect to abc.ABCMeta
    @type: obj: object
    @type: interface: abc.ABCMeta
    @rtype: str
    """
    for name in interface.__abstractmethods__:
        if not has_concrete_method(obj, name):
            yield name


def has_concrete_method(obj, name):
    """
    @type: obj: object
    @type: name: str
    @returns: bool
    """
    if hasattr(obj, name):
        return not is_abstract_method(getattr(obj, name))
    return False


def is_abstract_method(method):
    """
    @type: method: object
    @param: A method object.
    """
    return getattr(method, '__isabstractmethod__', False)



# ===================================
# interface_type.py
# ===================================
@six.add_metaclass(ValueMeta)
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


# ===================================
# validate.py
# ===================================


# ===================================
# valueabc.py
# ===================================

# ===================================
# valuemeta.py
# ===================================

# ===================================
# examples.py
# ===================================

# ===================================
# test_funkyvalidate.py
# ===================================



