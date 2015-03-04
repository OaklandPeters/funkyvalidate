"""
this is a refinement of the validate() function, to more cleanly handle
varieties of inner-type-checking (~Algebraic types).

It hinges on there being multiple possible keywords for approaches to
inner-type, in a way that parallels the type-hinting PEP 484, in that
it is based on the protocols from collections (Sequence, Iterator, Mapping)

validate(
    value,
    outer,
    sequence = Optional(TypeSpec),
    iterator = Optional(TypeSpec),
    mapping = Optional(TypeSpec),
)

TypeSpec = Union(type, Sequence[type])


@todo: Write a Nested class that captures the same structure as validate
@todo: write SequenceOf() as class or metaclass function
@todo: write Nested() as class or metaclass function
@todo: Prevent specifying more than one at a time of sequence, iterable, mapping
"""
import abc
from collections import Iterator, Mapping, Sequence
import six

from onefile import ValueABC


class Nested(ValueABC):
    #sequence = abstractclassmethod()
    #iterator = abstractclassmethod()
    #mapping = abstractclassmethod()
    @classmethod
    def __subclasscheck__(cls, subclass):
        return issubclass(subclass, cls.category)
    @classmethod
    def __instancecheck__(cls, instance):
        return is_valid(
            instance,
            cls.category,
            sequence=cls.sequence,
            iterator=cls.iterator,
            mapping=cls.mapping
        )


def nested(category, sequence=None, iterator=None, mapping=None):
    class NestedCls(Nested):
        category = category
        sequence = sequence
        iterator = iterator
        mapping = mapping
    return NestedCls


def validate(value, category, name='object', sequence=None, iterator=None, mapping=None):
    """
    Important structural points:
    (1) this is the point where keyword arguments are checked (other functions pass them through)
    (2) Importantly - returns the value, as this is necessary for...
    """
    result = validate_atomic(value, category=category, name=name)

    if sequence is not None:
        validate_sequence(value, sequence, name=name)

    if iterator is not None:
        result = validate_iterator(value, iterator, name=name)

    if mapping is not None:
        validate_mapping(value, mapping, name=name)

    return result

def is_valid(value, category, **keywords):
    try:
        validate(value, category, **keywords)
    except ValidationError:
        return False
    return True


def validate_atomic(value, category=None, name="object"):
    """
    Validates object, without considering types of 'inner'
    iterable elements.
    @type: value: Any
    @type: category: Optional[Validator, type]
    @type: name: Optional[str]
    @rtype: Any
    """
    if hasattr(category, 'validate'):
        result = category.__validate__(value)
    elif isinstance(category, type):
        result = type_check(value, category, name)
    elif category is None:  # Should this be here?
        result = value
    elif isinstance(category, tuple):
        # A tuple of types. Ex. isinstance(myvar, (NoneType, str))
        for i, elm in enumerate(category):
            validate(elm, type, name="{0}[{1}]".format(name, i))
        result = type_check(value, category, name)
    else:
        raise TypeError(
            _complaint(category, (Validator, type, None), "category")
        )
    return result


def validate_iterator(iterator, outer, **keywords):
    """
    Two possible ways this could be built:
    (1) return a new iterator, which implements the promise
    (2) monkey-patch iterator methods: next and/or __iter__
        This is a touchy issue. Most correct is overriding
        __iter__, and trusting .next to rely on that.

    @type: iterator: Iterator
    @type: outer: TypeSpec
    @type: keywords: Mapping
    @rtype: Iterator
    """
    type_check(iterator, Iterator, keywords.get('name', 'object'))
    return promises(iterator, outer, **keywords)


def validate_sequence(sequence, category, name='object', **keywords):
    """
    Returns value, unmodified
    @type: mapping: Sequence
    @type: category: Sequence[TypeSpec]
    @type: name: Optional[str]
    @type: keywords: Mapping
    @rtype: Sequence
    """
    type_check(sequence, Sequence, keywords.get('name', 'object'))

    name = keywords.get('name', 'object')
    for i, elm in enumerate(sequence):
        validate(elm, category, name="{0}[{1}]".format(name, i))
    return sequence


def validate_mapping(mapping, category, name='object', **keywords):  # pylint: disable=unused-argument
    """
    @type: mapping: Mapping
    @type: category: Sequence[TypeSpec]
    @type: name: Optional[str]
    @type: keywords: Mapping
    @rtype: Mapping
    """
    # Input validation
    type_check(mapping, Mapping, 'mapping')
    type_check(category, Sequence, 'category')
    if not len(category) == 2:
        raise TypeError(str.format(
            "'category' must be a Sequence of length 2, not length {0}.",
            len(category)
        ))
    keys_type, values_type = category
    type_check(keys_type, TypeSpec, 'category')
    type_check(values_type, TypeSpec, 'category')

    for key in mapping:
        value = mapping[key]
        validate(key, keys_type, name="{0} key '{1}'".format(name, key))
        validate(value, values_type, name="{0}[{1}]".format(name, key))

    return mapping


def promises(iterable, outer, **keywords):
    """
    @type: iterable
    """
    for i, elm in enumerate(iterable):
        kwargs = _update_name_in_keywords(i, keywords)
        yield validate(elm, outer, **kwargs)




def _update_name_in_keywords(index, keywords):
    """
    Update 'name' keyword with sequence identifier. Does not mutate keywords.
    @type: index: Any
    @type: keywords: Mapping
    @rtype: Mapping
    """
    name = keywords.get('name', None)
    if name is None:
        name = 'object'
    name = str.format("{0}[{1}]", name, index)
    return dict(
        keywords.items(),
        ('name', name)
    )





@six.add_metaclass(abc.ABCMeta)
class Validator(object):
    """Interface for objects implementing the __validate__ protocol."""
    __validate__ = abc.abstractmethod(lambda: NotImplemented)

from onefile import ValueABC

class TypeSpec(ValueABC):
    """Run-time type checking for valid 2nd arguments to isinstance/issubclass
    """
    @classmethod
    def __instancecheck__(cls, instance):
        if isinstance(instance, type):
            return True
        elif isinstance(instance, Sequence):
            if all(isinstance(elm, type) for elm in instance):
                return True
        return False

    @classmethod
    def __subclasscheck__(cls, subclass):
        """Revert to standard inheritance-tree checking...
        This might POSSIBLY need to be instead:
        type.__instancecheck__(cls, subclass)
        """
        return abc.ABCMeta.__instancecheck__(cls, subclass)


class SequenceOf(ValueABC):
    """
    TypeSpec = Union(type, Sequence[type])
    """
    def __new__(cls, typespec):
        """Uncompleted"""
        new_cls = type('', typespec, {})
        return new_cls

    @classmethod
    def construct(cls, typespec):
        """Alternate constructor method."""
        type_check(typespec, TypeSpec, 'typespec')  # Union[type, Sequence[type]]
        if isinstance(typespec, type):
            name = "SequenceOf" + type.__name__
        else:  # isinstance(typespec, Sequence):
            name = "SequenceOfUnion"
        return type(name, (SequenceOf, ), {'typespec': typespec})
    @classmethod
    def __instancecheck__(cls, instance):
        return isinstance(instance, cls.typespec)


# ---------------- Material shared from old validate.py
class ValidationError(TypeError):
    """Basic exception type."""
    pass

def _non_string_sequence(obj):
    """type_check for non-string sequences."""
    return isinstance(obj, Sequence) and not isinstance(obj, basestring)

def _complaint(value, types, name):
    """Sugar for generating exception messages."""
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

def type_check(value, category, name):
    """
    Primitive function for raises validation errors based on
    run-time type-checking.
    """
    if not isinstance(value, category):
        raise ValidationError(_complaint(value, category, name))
    return value


