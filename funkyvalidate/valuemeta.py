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

@todo: ValueMeta can get caught in recursive loops. See if it is possible to more cleanly prevent this.
@todo: Consider removing the instances contained here (ExistingFile, ExistingDirectory, PositiveInteger) - to their own files
@todo: Determine: Will ValueABC.__instancecheck__ classmethod will disrupt the ValueMeta.__instancecheck__ ?
"""
import abc
import os

import six

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

    # ! INTENT is...
    # This should be method on the class descendants of value-interface,
    # ... but not appear on the instances of that class
    # 
    # ... can I achieve this via a classmethod on the metaclass?
    def _assert(cls, instance, **keywords):

        # Chain: keyword, cls attribute, default
        exc_type = keywords.get('exception',
            default=getattr(cls, 'exception',
                default=ValueABCAssertionError)) #

        getattr(cls, 'exception')
        if not isinstance(instance, cls):
            exc_type = getattr(cls, 'exception', default=ValueABCAssertionError)
            raise exc_type(str.format(
                "Invalid"
            ))



def _hasattr(C, attr):
    try:
        return any(attr in B.__dict__ for B in C.__mro__)
    except AttributeError:
        # Old-style class
        return hasattr(C, attr)

class abstractclassmethod(classmethod):

    __isabstractmethod__ = True

    def __init__(self, callable):
        callable.__isabstractmethod__ = True
        super(abstractclassmethod, self).__init__(callable)





class ValueABC(object):
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
    __metaclass__ = ValueMeta

    @abstractclassmethod
    def __instancecheck__(cls, instance):
        return NotImplemented


