"""
Single file version.

"""

import collections
import abc
import six
import types

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
# shared.py
# ===================================
def _hasattr(C, attr):
    try:
        return any(attr in B.__dict__ for B in C.__mro__)
    except AttributeError:
        # Old-style class
        return hasattr(C, attr)
 


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
# valuemeta.py
# ===================================
class ValueMeta(abc.ABCMeta):
    """
    Classes inheriting from ValueABC should be used for type hinting,
    annotations, and sometimes type-checking.

    IE Functional-language type-checking, not OOP-style type checking
    Somewhat similar to the way that types are used in more functional languages.

    Pythonicaly, when used as a type-annotation in a docstring annotation, the class implied
    should bear the right methods (~as an interface), but it can ALSO be used as part of:
        isinstance(obj, value_interface)
    ... to confirm that the value is correct.

    Pythonically, what it DOES NOT do:
    Check the value when you create it. Value/type checking must be done explictly.

    @todo: Determine: Will ValueABC.__instancecheck__ classmethod will disrupt the ValueMeta.__instancecheck__ ?
    """

    def __instancecheck__(cls, instance):
        if _hasattr(cls, '__instancecheck__'):
            #if (cls.__instancecheck__ == ValueMeta.__instancecheck__):
            return cls.__instancecheck__(instance)
        else:
            return abc.ABCMeta.__instancecheck__(cls, instance)

    def __subclasscheck__(cls, subclass):
        if _hasattr(cls, '__subclasscheck__'):
            return cls.__subclasscheck__(subclass)
        else:
            return abc.ABCMeta.__subclasscheck__(cls, subclass)


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

class Validator(InterfaceType):
    """
    Defines a new magic method and protocol.
    (Yes, I know magic methods)
    """
    __validate__ = abc.abstractmethod(lambda: NotImplemented)


# ===================================
# valueabc.py
# ===================================

class abstractclassmethod(classmethod):
    """abstractmethod, but for classmethods. Python 2 compatible.

    Python 3 provides this as abc.abstractclassmethod.
    Python 3.4 removes the need for this, by allowing @classmethod to be
        used with abstractmethod.

    """
    __isabstractmethod__ = True
    def __init__(self, callable):
        callable.__isabstractmethod__ = True
        super(abstractclassmethod, self).__init__(callable)


@six.add_metaclass(ValueMeta)
class ValueABC(object):
    """Bears ValueMeta, so it can more easily be added to classes
    in both Python 2 and Python 3, via standard inheritance.
    """
    @abstractclassmethod
    def __instancecheck__(cls, instance):
        return NotImplemented
    
    @abstractclassmethod
    def __instancecheck__(cls, instance):
        return NotImplemented


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
    elif category is None:  # Should this be here?
        return value
    elif isinstance(category, tuple):
        for i, elm in enumerate(category):
            validate(elm, type, name="{0}[{1}]".format(name, i))
        return type_check(value, category, name)
    else:
        raise ValidationError(
            _complaint(category, (Validator, type, None), "category")
        )

def is_valid(value, category=None):
    try:
        validate(value, category)
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


# ===================================
# pep484.py
# ===================================
class Any(ValueABC):
    """
    Back port of typing.Any from PEP 483, into a 2.7 implementation.
    This version of `Any` differs in some major ways. For example, this version
    does not count as a subclass of all other classes, but the true PEP 483 version
    does.
        assert isinstance(typing.Any, SomeClass)
        assert not isinstance(metatypes.Any, SomeClass)
    """
    @classmethod
    def __instancecheck__(cls, instance):  # pylint: disable=unused-argument
        """
        @type: instance: Any
        @rtype: bool
        """
        return True

    @classmethod
    def __subclasscheck__(cls, subclass):  # pylint: disable=unused-argument
        """
        @type: subclass: type
        @rtype: bool
        """
        return True


class UnionMeta(ValueMeta):
    """
    Metaclass for generating TypeUnion classes.

    UnionMeta(...)
    --> Union(...)
    --> TypeUnion(...)

    """
    def __new__(mcls, name, bases, namespace):
        """
        Union(list, tuple) -->
            TypeUnion = UnionMeta('TypeUnion', (,), {})
            return TypeUnion

        Triggers type.__new__, which will cause different behavior
        for descendants, if mcls has __instancecheck__ and __subclasscheck__

        Unconfirmed Belief: methods on mcls become classmethods on cls. Classmethods on mcls do not appear on cls at all.

        @todo: Requires that namespaces includes 'types', and validate it.

        @type: name: str
        @type: bases: Sequence[type]
        @type: namespace: dict[str, Any]
        """

        # Construct class - uses type.__new__
        cls = super(UnionMeta, mcls).__new__(mcls, name, bases, namespace)

        return cls

    def __call__(cls, *args, **kwargs):
        """
        Triggered whenever the newly created class is "called"
        to instantiate a new object.

        (mcls.__init__ controls the initialization of the new class,
         NOT the initialization of the instances of the new class)
        
        I need to set Union(list, tuple) to return a class
        ... this can be done either here in UnionMeta.__call__, or in Union.__new__
        """
        return cls.__new__(cls, *args, **kwargs)

    def __repr__(cls):
        return str.format(
            "<'{0}': {1}>",
            cls.__name__, repr(getattr(cls, 'utypes', ''))
        )

class ConcreteSet(collections.MutableSet):
    """
    Set-class, used by Union and Optional.
    Holds types, subject to set-theoretic operations.

    Will eventually be used by Intersection and Not.
    """
    def __init__(self, *data):
        self.data = set()
        for elm in data:
            self.add(elm)
    def __contains__(self, other):
        return other in self.data
    def __iter__(self):
        return iter(self.data)
    def __len__(self):
        return len(self)
    def add(self, value):
        self.data.add(validate_type(value))
    def remove(self, value):
        self.data.remove(value)


class UnionBase(ConcreteSet):
    __metaclass__ = UnionMeta
    @classmethod
    def __instancecheck__(cls, instance):                
        return any(
            isinstance(instance, _type)
            for _type in cls._types
        )
    @classmethod
    def __subclasscheck__(cls, subclass):
        return any(
            issubclass(subclass, _type)
            for _type in cls._types
        )


class Union(UnionBase):
    def __new__(cls, *utypes):
        """Create and return a new class inheriting from Union."""
        _types = handle_union_types(utypes)
        TypeUnion = type(
            'TypeUnion',
            (Union, ),
            {'_types': _types}
        )
        return TypeUnion


class Optional(Union):
    """
    `Optional[MyType]` is an alias of `Union[NoneType, MyType]`
    """
    def __new__(cls, *utypes):
        _types = tuple([types.NoneType]) + utypes
        return Union(*_types)


class Tuple(ConcreteSet):
    """
    A tuple whose instances match the types passed into the constructor for Tuple.
    """
    @classmethod
    def __instancecheck__(cls, instance):
        """
        Element-by-element comparison for equal-length tuples; otherwise false.
        @type: instance: Any
        @rtype: bool
        """
        if isinstance(instance, tuple):
            if len(instance) == len(cls.types):
                return all(
                    isinstance(element, _type)
                    for element, _type
                    in zip(instance, cls.types)
                )
            else: # not same length
                return False
        else:  # not a tuple
            return False
    @classmethod
    def __subclasscheck__(cls, subclass):
        """
        @type: subclass: type
        @rtype: bool
        """
        if issubclass(subclass, tuple):
            if len(subclass) == len(cls._types):
                return all(
                    issubclass(element, _type)
                    for element, _type
                    in zip(subclass, cls._types)
                )
            else: # not same length
                return False
        else:  # not a tuple
            return False


# ===================================
# handlers.py
# ===================================
def handle_union_types(union_types):
    """
    @type: union_types: Sequence[Optional[type]]
    @rtype: 
    """
    _types = handle_empty_types(union_types)
    # [] Unfold any nested Unions
    _types = tuple(handle_nested_unions(_types))
    # [] Convert None to NoneType
    _types = tuple(handle_none_type(_types))
    # [] Validate input
    _types = tuple(validate(element, type) for element in _types)
    return _types


def handle_nested_unions(_types):
    """Recursively unfolds unions into a flattened sequence of types.
    @type: _types: Sequence[type]
    @rtype: Iterator[type]
    """
    for element in _types:
        if not _hasattr(element, '_types'):
            yield element
        else:
            for inner in handle_nested_unions(element._types):
                yield inner

def handle_empty_types(_types):
    """
    @type: _types: Sequence[Optional[type]]
    @rtype: Sequence[type]
    """
    if len(list(_types)) == 0:
        return tuple([Any])
    else:
        return _types

def handle_none_type(_types):
    """
    @type: _types: Iterable
    @rtype: Iterator[type]
    """
    for element in _types:
        if element is None:
            yield types.NoneType
        else:
            yield element
