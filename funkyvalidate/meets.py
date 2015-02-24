"""
Defines the 'meets' function - which is used to check if an object or class
satisifies the abstract methods on an interface.
"""

__all__ = [
    'meets'
]

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
