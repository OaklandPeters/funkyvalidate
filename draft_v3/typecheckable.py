"""

"""
import abc
import six

def _hasattr(C, attr):
    try:
        return any(attr in B.__dict__ for B in C.__mro__)
    except AttributeError:
        # Old-style class
        return hasattr(C, attr)

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

class TypeCheckableMeta(abc.ABCMeta):
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





@six.add_metaclass(TypeCheckableMeta)
class TypeCheckable(object):
    """Bears ValueMeta, so it can more easily be added to classes
    in both Python 2 and Python 3, via standard inheritance.
    """
    @abstractclassmethod
    def __instancecheck__(cls, instance):
        return NotImplemented
    
    @abstractclassmethod
    def __instancecheck__(cls, instance):
        return NotImplemented
