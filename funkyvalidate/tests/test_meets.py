import unittest
import abc

from funkyvalidate import is_abstract_method, has_concrete_method, missing_abstracts, meets


# Support object
class ValidatorInterface(object):
    __metaclass__ = abc.ABCMeta
    exception = abc.abstractproperty(lambda *args, **kwargs: NotImplemented)
    message = abc.abstractmethod(lambda *args, **kwargs: NotImplemented)
    __instancecheck__ = abc.abstractmethod(lambda *args, **kwargs: NotImplemented)

    def validate(self, obj, name="object"):
        """Mixin - non-abstract method."""
        if self.__instancecheck__(self, obj):
            raise self.exception(
                self.message(obj, name=name)
            )
        return obj


class MyValidator(object):
    exception = TypeError
    def message(self, obj, name=None):
        pass
    def __instancecheck__(self, other):
        pass

class NotAValidator(object):
    """Already inherits __instancecheck__ from object"""
    exception = RuntimeError


class MeetsTests(unittest.TestCase):
    """
    Tests for functions to be contained in meets.py
    """

    def test_is_abstract_method(self):
        self.assertTrue(is_abstract_method(ValidatorInterface.exception))
        self.assertTrue(is_abstract_method(ValidatorInterface.message))
        self.assertFalse(is_abstract_method(ValidatorInterface.validate))

    def test_has_concrete_method(self):
        self.assertTrue(not has_concrete_method(ValidatorInterface, 'exception'))
        self.assertTrue(not has_concrete_method(ValidatorInterface, 'message'))

        self.assertTrue(has_concrete_method(ValidatorInterface, 'validate'))

    def test_missing_abstracts(self):
        self.assertEqual(
            set(missing_abstracts(MyValidator, ValidatorInterface)),
            set([])
        )
        self.assertEqual(
            set(missing_abstracts(NotAValidator, ValidatorInterface)),
            set(['message'])
        )

    def test_meets(self):
        self.assertTrue(meets(MyValidator, ValidatorInterface))
        self.assertTrue(not meets(NotAValidator, ValidatorInterface))


if __name__ == "__main__":
    unittest.main()
