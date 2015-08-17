"""
Types used by test_merge_model
"""
import collections

import django.db.models.base # pylint: disable=import-error
import apps.authors.models # pylint: disable=import-error

from validate import validate, is_valid
from typecheckable import TypeCheckable

__all__ = [
    'ModelType',        # type = django.db.models.base.ModelBase
    'ModelObject',      # type = django.db.models.base.Model
    'AuthorType',       # type = author.models.Author
    'FieldValue',       # type = Tuple[str, Any]
    'RawPair',          # type = Tuple[FieldValue, FieldValue]
    'ModelPair',        # type = Tuple[ModelObject, ModelObject]
    'FieldSequence',    # type = Sequence[Fieldvalue]
    'ModelSequence',    # type = Sequence[ModelObject]
]

# Type Definitions
ModelType = django.db.models.base.ModelBase
ModelObject = django.db.models.base.Model
AuthorType = apps.authors.models.Author


class FieldValue(tuple, TypeCheckable):
    """type = Tuple[str, Any]"""
    @classmethod
    def __instancecheck__(cls, instance):
        if isinstance(instance, tuple):
            if len(instance) == 2:
                if isinstance(instance[0], str):
                    return True
        return False

    @classmethod
    def __subclasscheck__(cls, subclass):
        if isinstance(subclass, tuple):
            return True
        return False


    def __new__(cls, name, value):
        validate(name, str)
        validate(value, object)
        return super(RawPair, cls)








class RawPair(tuple, TypeCheckable):
    """type = Tuple[FieldValue, FieldValue]"""
    @classmethod
    def __instancecheck__(cls, pair):
        if isinstance(pair, tuple):
            if len(pair) == 2:
                if isinstance(pair[0], FieldValue) and isinstance(pair[1], FieldValue):
                    return True
        return False

    @classmethod
    def __subclasscheck__(cls, subclass):
        if isinstance(subclass, tuple):
            return True
        else:
            return False

    def __new__(cls, first, second):
        validate(first, FieldValue)
        validate(second, FieldValue)
        return super(RawPair, cls).__new__(cls, [first, second])


class ModelPair(tuple, TypeCheckable):
    """
    type = Tuple[ModelObject, ModelObject]
    """
    @classmethod
    def __instancecheck__(cls, pair):
        if isinstance(pair, tuple):
            if len(pair) == 2:
                if isinstance(pair[0], ModelObject) and isinstance(pair[1], ModelObject):
                    return True
        return False
    @classmethod
    def __subclasscheck__(cls, subclass):
        if isinstance(subclass, tuple):
            return True
        else:
            return False

    def __new__(cls, first, second):
        validate(first, ModelObject)
        validate(second, ModelObject)
        return super(ModelPair, cls).__new__(cls, [first, second])






class FieldSequence(tuple, TypeCheckable):
    """
    type = Sequence[FieldValue]
    """
    @classmethod
    def __instancecheck__(cls, instance):
        return is_valid(instance, category=collections.Sequence, inner=FieldValue)

    @classmethod
    def __subclasscheck__(cls, subclass):
        return issubclass(subclass, collections.Sequence)

class ModelSequence(tuple, TypeCheckable):
    """
    type = Sequence[ModelObject]
    """
    @classmethod
    def __instancecheck__(cls, instance):
        return is_valid(instance, category=collections.Sequence, inner=ModelObject)

    @classmethod
    def __subclasscheck__(cls, subclass):
        return issubclass(subclass, collections.Sequence)
