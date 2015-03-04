"""
"""
import unittest
import collections

from funkyvalidate import Any, Union, UnionMeta

class MyClass(object):
    pass
class MyTuple(tuple):
    pass


class AnyTestCase(unittest.TestCase):
    """
    Unit-tests for the Any class.
    """
    def test_instancecheck(self):
        self.assertTrue(isinstance(12, Any))
        self.assertTrue(isinstance('ba', Any))
        self.assertTrue(isinstance(['ba'], Any))
        self.assertTrue(isinstance(None, Any))
        self.assertTrue(isinstance(type(None), Any))
        self.assertTrue(isinstance(map, Any))
        self.assertTrue(isinstance(dict, Any))
        self.assertTrue(isinstance(lambda: NotImplemented, Any))
        self.assertTrue(isinstance(NotImplemented, Any))

        self.assertTrue(isinstance(MyClass, Any))
        self.assertTrue(isinstance(MyClass(), Any))
        
    def test_subclasscheck(self):
        """Confirm that issubclass({{x}}, Any) works."""
        self.assertTrue(issubclass(type(None), Any))
        self.assertTrue(issubclass(dict, Any))
        self.assertTrue(issubclass(MyClass, Any))

        valid = [
            MyClass(), 12, 'ba', ['ba'], tuple(), None, map,
            lambda: NotImplemented, NotImplemented
        ]
        for obj in valid:
            self.assertTrue(obj, Any)
            # with self.assertRaises(TypeError):
            #     issubclass(obj, Any)

class TargetedTestCase(unittest.TestCase):
    def test_basic(self):
        self.assertFalse(issubclass(Union(list, tuple), list))


# class UnionTestCase(unittest.TestCase):
#     def test_direct_class(self):
#         combined = Union(list, tuple)

#         # self.assertFalse(isinstance(combined, Union))
#         self.assertTrue(issubclass(combined, Union))

# #        self.assertFalse(isinstance(Union, combined))
#         self.assertFalse(issubclass(Union, combined))

#         # self.assertFalse(isinstance(Union, Union))
#         self.assertTrue(issubclass(Union, Union))

#         # self.assertFalse(isinstance(combined, combined))
#         self.assertFalse(issubclass(combined, combined))

#     def test_single_types(self):
#         single = Union(list)
#         self.assertTrue(issubclass(Union(list), list))
#         self.assertTrue(issubclass(list, Union(list)))

#         self.assertTrue(isinstance("", Union(str)))
#         self.assertFalse({}, Union(tuple))
#         with self.assertRaises(TypeError):
#             isinstance(Union(str), "")

#         self.assertFalse(isinstance(Union(str), str))
#         self.assertFalse(isinstance(str, Union(str)))

#     def test_empty(self):
#         empty = Union()
#         self.assertEqual(empty._types, tuple([Any]))
#         self.assertTrue(isinstance([], empty))
#         self.assertTrue(issubclass(type(None), empty))

    # def test_self_reference(self):
    #     combined = Union(Union, list)

    #     self.assertTrue(issubclass(combined, Union))
    #     self.assertTrue(issubclass(combined, combined))
    #     self.assertTrue(issubclass(Union, combined))

    #     self.assertFalse(isinstance(combined, Union))
    #     self.assertFalse(isinstance(combined, combined))
    #     self.assertFalse(isinstance(Union, combined))

    # def test_isinstance(self):
    #     combined = Union(list, tuple)

    #     self.assertTrue(isinstance([], combined))
    #     self.assertTrue(isinstance([12, 32], combined))
    #     self.assertTrue(isinstance(tuple(), combined))
    #     self.assertTrue(isinstance(MyTuple(), combined))

    #     self.assertFalse(isinstance(tuple, combined))
    #     self.assertFalse(isinstance(list, combined))
    #     self.assertFalse(isinstance("asa", combined))
    #     self.assertFalse(isinstance(str, combined))
    #     self.assertFalse(isinstance(None, combined))

    # def test_issubclass(self):
    #     combined = Union(list, tuple)

    #     self.assertTrue(issubclass(str, combined))
    #     self.assertTrue(issubclass(list, combined))
    #     self.assertTrue(issubclass(MyTuple, combined))

    #     self.assertFalse(issubclass(None, combined))
    #     self.assertFalse(issubclass(type(None), combined))
    #     self.assertFalse(issubclass(MyClass, combined))
    #     from collections import Sequence
    #     self.assertFalse(issubclass(Sequence, combined))
    #     self.assertFalse(issubclass(dict, combined))

    #     with self.assertRaises(TypeError):
    #         issubclass(MyClass(), combined)
    #     
    #     self.assertFalse(issubclass(combined, list))
    #     self.assertFalse(issubclass(combined, tuple))
    #     self.assertFalse(issubclass(combined, (tuple, list))
    def test_union_to_union(self):
        base = Union(list, tuple, str)
        smaller = Union(list, tuple)
        larger = Union(list, tuple, str, dict)
        overlap = Union(list, tuple, set)
        nonoverlap = Union(dict, bool)
        ancestor = Union(collections.Sequence, bool)

        self.assertFalse(issubclass(base, smaller))
        self.assertTrue(issubclass(smaller, base))

        self.assertTrue(issubclass(base, larger))
        self.assertTrue(issubclass(larger, base))

        self.assertTrue(issubclass(base, overlap))
        self.assertTrue(issubclass(overlap, base))

        self.assertFalse(issubclass(base, nonoverlap))
        self.assertFalse(issubclass(nonoverlap, base))

        self.assertTrue(issubclass(base, ancestor))
        self.assertFalse(issubclass(ancestor, base))

    #     self.assertTrue(issubclass(combined, Union(list, tuple, )))


# class ReverseTestCase(unittest.TestCase):
#     def test_basic(self):
#         combined = Union(list, tuple)
#         self.assertTrue(issubclass(combined, collections.Sequence))
#         # Currently this errors because Union produces an instance, not a class

if __name__ == "__main__":
    unittest.main()
