"""
Convenience for run-time (isinstance) type-checking structured & nested data.
"""
from valueabc import ValueABC
from validate import is_valid

# def Nested(category, inner):
#     """
#     Class constructor.

#     raw_pairs = ((('slug', 'phoebe-adams'), ('slug', 'phoebe-lou-adams')),)

#     isinstance(raw_pairs, Nested(tuple, Nested(tuple, Nested(tuple, str))))
#     True
#     isinstance(raw_pairs, Nested(tuple, Nested(tuple, Nested(tuple, bool))))
#     False
#     """
#     # @todo: check category & inner: Union[type, tuple[type]]

#     class NestedClass(ValueABC):
#         _outer = category
#         _inner = inner
#         @classmethod
#         def __instancecheck__(cls, instance):
#             return is_valid(instance, category=cls._outer, inner=cls._inner)

#         @classmethod
#         def __subclasscheck__(cls, subclass):
#             return issubclass(subclass, cls._outer)
#     NestedClass.__name__ = "Nested" + category.__name__
#     return NestedClass

class Nested(ValueABC):
    """
    Example nesting structure.
    However, this only works with single class structure(ie outer and inner cannot be tuples of classes)
    """
    def __new__(cls, outer, inner):
        return cls.inherit(outer, inner)

    @classmethod
    def inherit(cls, outer, inner):
        name = "".join(
            part.capitalize() for part in 
            (outer.__name__, "of", inner.__name__)
        )
        bases = (Nested, )
        namespace = {
            '_outer': outer,
            '_inner': inner
        }
        cls = type(name, bases, namespace)

        return cls


    @classmethod
    def __instancecheck__(cls, instance):
        if cls is Nested:
            return is_ancestor(cls, type(instance))
        else:
            return is_valid(instance, category=cls._outer, inner=cls._inner)

    @classmethod
    def __subclasscheck__(cls, subclass):
        if cls is Nested:
            return is_ancestor(cls, subclass)
        else:
            return issubclass(subclass, cls._outer)


def is_ancestor(cls, subclass):
    """
    @type: cls: type
    @type: subclass: type
    @rtype: bool
    """
    try:
        return cls in subclass.__mro__
    except AttributeError:
        # raise same exception as issubclass(instance, klass)
        raise TypeError(str.format(
            "argument 1 must be a class."
        ))


import unittest

class NestedTests(unittest.TestCase):
    def test_basic(self):
        from collections import Sequence, Iterable, Iterator
        mynested = Nested.inherit(Sequence, str)
        print()
        print("mynested:", type(mynested), mynested)
        print()
        import pdb
        pdb.set_trace()
        print()

