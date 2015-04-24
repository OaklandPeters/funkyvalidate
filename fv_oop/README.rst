funky-validate-oop
====================

Overview
----------
This is notes, stubs, and prototypes of a more structure and complex version of
the validation ideas behind funkyvalidate. It is not intended for use, at least
not yet.

Key Goals
-----------
- Nesting Support   (~Algebraic types)



Core Desires
--------------
- All validation here can be turned off with the same flag used to turn off asserts.
- Standardized exception types.
    - ValidationError(AssertionError)
    - ValidationTypeError(TypeError, ValidationError)
    - ValidationValueError(ValueError, ValidationError)
    - ... something for errors involving checking the file system (Existing files, directories...)
- Should have a structure to abstract the name/message passing part of validation
- Magic methods (or equivalent) for core tasks
- NESTING SUPPORT (as in clever_validate.py)
    - validate : sequence (~recursive check), mapping (key-value), iterator (promises)
        - write as classes, that provide a special iterator/mapper method
            - used to iterate over some object appropriately. (see Example #1)

    - validate_atomic : this is normal validation
- Supporting ABCs:
    - InterfaceType
    - Atomic
    - TypeCheckable/TypeCheckableMeta  (interface checking + value checking support)
    - Any
- Examples of uses: value types
    - ExistingFile/ExistingDirectory
    - PositiveInteger
- Unit-tests which check:
    - For bad recursion
    - For correct inheritance

Example #1
------------
validate(value, outer, inner=validate.Mapping(str, validate.Sequence), name='value')
--> 
if inner is not None:
    for elm, inner_category, inner_name in inner.wrap(value, name=name).__iterate__():
        # inner_category would be validate.Sequence
        # inner_name = "{0}[{1}]".format(name, i)
        validate(elm, inner_category, name=inner_name)


Magic Methods
---------------
Core validation related magic methods - ideas:
    - __validate__ : __validate__(self, value, name) --> value or raise ValidationError
    - __check__ : __check__(self, value) --> bool
        - Is this different than isinstance?


Types of Validation
---------------------
- Type check on basic types
    - On inheritance (classic Python)
    - On abstract inheritance (extended Python)
        - Requires support (ie `meets(obj, interface)`)
- Value-type check, on 
