
from .validate import is_valid
from .typecheckable import TypeCheckable

# Speculative

def Nested(category, inner):
    """
    Class constructor.

    raw_pairs = ((('slug', 'phoebe-adams'), ('slug', 'phoebe-lou-adams')),)

    isinstance(raw_pairs, Nested(tuple, Nested(tuple, Nested(tuple, str))))
    True
    isinstance(raw_pairs, Nested(tuple, Nested(tuple, Nested(tuple, bool))))
    False
    """
    # @todo: check category & inner: Union[type, tuple[type]]

    class NestedClass(TypeCheckable):
        _outer = category
        _inner = inner
        @classmethod
        def __instancecheck__(cls, instance):
            return is_valid(instance, category=cls._outer, inner=cls._inner)

        @classmethod
        def __subclasscheck__(cls, subclass):
            return issubclass(subclass, cls._outer)
    NestedClass.__name__ = "Nested" + category.__name__
    return NestedClass
