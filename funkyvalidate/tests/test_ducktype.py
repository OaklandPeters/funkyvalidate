import unittest
import abc

import meets

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

    def test_is_abstract_method(self):
        self.assertTrue(meets.is_abstract_method(ValidatorInterface.exception))
        self.assertTrue(meets.is_abstract_method(ValidatorInterface.message))

        self.assertTrue(not meets.is_abstract_method(ValidatorInterface.validate))

    def test_has_concrete_method(self):
        self.assertTrue(not meets.has_concrete_method(ValidatorInterface, 'exception'))
        self.assertTrue(not meets.has_concrete_method(ValidatorInterface, 'message'))

        self.assertTrue(meets.has_concrete_method(ValidatorInterface, 'validate'))

    def test_missing_abstracts(self):
        self.assertEqual(
            set(meets.missing_abstracts(MyValidator, ValidatorInterface)),
            set([])
        )
        self.assertEqual(
            set(meets.missing_abstracts(NotAValidator, ValidatorInterface)),
            set(['message'])
        )

    def test_meets(self):
        self.assertTrue(meets.meets(MyValidator, ValidatorInterface))
        self.assertTrue(not meets.meets(NotAValidator, ValidatorInterface))

if __name__ == "__main__":
    unittest.main()
