"""
@todo: Remove inner_category from being passed by mapper
"""

from abc import abstractproperty, abstractmethod

class Any(object):
    """Stub."""

class NestedValidator(object):

    @abstractmethod
    def __init__(self, outer, name="object", inner=Any):
        """
        This may validate inner - such as for Mapping,
        which requires specying (Key, Values)
        """
        self.outer_name = name
        self.outer_category = outer
        self.inner_category = inner
    
    outer_name = abstractproperty()
    inner_category = abstractproperty()
    outer_category = abstractproperty()
    @abstractmethod
    def mapper(self, value):
        """
        @rtype: Tuple[Any, TypeSpec, str]
        @returns: (elm, category, name)
        """
        return NotImplemented

    @abstractmethod
    def validate(self, value):
        return NotImplemented

    def validate(self, value):
        validate(value, self.outer_category, name=self.name)
        for elm, inner_category, inner_name in self.mapper(value):
            validate(elm, inner_category, name=inner_name)


class Sequence(NestedValidator):
    def mapper(self, value):
        for i, elm in enumerate(value):
            inner_name = "{0}[{1}]".format(self.outer_name, i)
            yield (elm, self.inner_category, inner_name)

class Mapping(NestedValidator):
    def __init__(self, outer, name="object", inner=(Any, Any)):
        # Validate inner
        validate_atomic(inner, collections.Sequence, name="inner")
        validate_sequence(inner, TypeSpec, name="inner")
        validate_length(inner, 2, name="inner")
        super(NestedValidator, self).__init__(outer, name=name, inner=inner)

    @property
    def inner_key(self):
        return self.inner_category[0]
    @property
    def inner_value(self):
        return self.inner_category[1]

    def mapper(self, value):
        for key in value:
            elm = value[elm]
            inner_name = "{0}[{1}]".format(self.outer_name, i)
            yield (elm, self.inner_category, inner_name)

class Iterator(NestedValidator):
    def mapper(self, value):
        for i, key in enumerate(value):
            inner_name = "{0}[{1}]"format(self.outer_name, i)
            yield (elm, self.inner_category, inner_name)
