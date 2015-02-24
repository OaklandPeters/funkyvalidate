import os

import six

from ..valuemeta import ValueMeta

# Examples
@six.add_metaclass(ValueMeta)
class ExistingDirectory(str):
    # __metaclass__ = ValueMeta

    @classmethod
    def __instancecheck__(cls, instance):
        if isinstance(instance, basestring):
            if os.path.isdir(instance):
                return True
        return False

@six.add_metaclass(ValueMeta)
class PositiveInteger(int):
    # __metaclass__ = ValueMeta
    @classmethod
    def __instancecheck__(cls, instance):
        if isinstance(instance, int):
            if instance > 0:
                return True
        return False

    def __new__(cls, *args, **kwargs):
        self = int(*args, **kwargs)
        if not isinstance(self, cls):
            raise
