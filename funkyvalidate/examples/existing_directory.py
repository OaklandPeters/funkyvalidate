import os

from funkyvalidate import ValueMeta

class ExistingDirectory(str):
    """
    Non-instanced type-checking class (a VOG).
    """
    __metaclass__ = ValueMeta
    def __init__(self, value):
        cls = type(self)
        if not cls.__instancecheck__(value):
            raise cls._exception_(value)
        super(cls, self).__init__(value)

    @classmethod
    def __instancecheck__(cls, instance):
        if isinstance(instance, basestring):
            if os.path.isdir(instance):
                return True
        return False

    @classmethod
    def _exception_(cls, instance):
        if isinstance(instance, basestring):
            return IOError(str.format(
                "Cannot find a directory at location '{0}'.",
                instance
            ))
        else:
            return TypeError(str.format(
                "Object of type {0} should be basestring.",
                type(instance).__name__
            ))
