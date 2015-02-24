
Refactor
-----------
- Rename ValueMeta/ValueABC --> TypeCheckable and TypeCheckable
- metatypes: Allow Union and validate to accept 'None', and validate it into NoneType.
- metatypes: Simplification inside Union: Union(single)-->single
- metatypes: Simplification inside Union: Union(A, Union(B, C))-->Union(A, B, C)

Bugs
-----------
- Recursive loops occur when Union is used to instance/subclass check itself, and likely also when it is used on an inheritor (eg. isinstance(Union(NoneType, dict), Union))
