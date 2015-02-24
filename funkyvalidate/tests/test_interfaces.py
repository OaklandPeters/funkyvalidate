import os
import unittest
import abc

from existing_directory import ExistingDirectory
from existing_file import ExistingFile
from interface_type import InterfaceType

class InterfaceTests(unittest.TestCase):
    def test_existingdirectory(self):
        self.assert_(isinstance('test_bypath', ExistingDirectory))
        self.assert_(not isinstance('_test_bypath', ExistingDirectory))

        self.assert_(os.path.exists('__init__.py'))
        self.assert_(not isinstance('__init__.py', ExistingDirectory))

    def test_existingfile(self):


        self.assert_(isinstance('__init__.py', ExistingFile))
        self.assert_(ExistingFile('__init__.py') == '__init__.py')
        self.assertRaises(TypeError, lambda: ExistingFile(12))
        self.assertRaises(IOError, lambda: ExistingFile('wargarbl'))


class InterfaceTypeTests(unittest.TestCase):
    def test_meets(self):
        class MyInterface(InterfaceType):
            @abc.abstractproperty
            def first_name(self):
                pass

        class YesClass(object):
            def __init__(self):
                pass
            first_name = "foo"
        yes = YesClass()

        class AlsoClass(object):
            def __init__(self):
                self.first_name = "bar"
        also = AlsoClass()

        class NoClass(object):
            pass
        no = NoClass()

        self.assertTrue(isinstance(yes, MyInterface))
        self.assertTrue(isinstance(also, MyInterface))
        self.assertFalse(isinstance(no, MyInterface))


if __name__ == "__main__":
    unittest.main()
