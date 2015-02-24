
Refactor
-----------
- Rename ValueMeta/ValueABC --> TypeCheckable and TypeCheckable


Features
-----------
- metatypes: Allow Union and validate() to accept 'None', and validate it into NoneType.
- metatypes: Simplification inside Union: Union(single)-->single
- metatypes: Simplification inside Union: Union(A, Union(B, C))-->Union(A, B, C)
- Validator & validate: __validate__ --> validate: only core Python devs should define magic methods.


Packaging
-----------
- Add git tag: 0.1
- Fill in kruft: setup.py
- Fill in kruft: README_TEMPLATE.rst: Motivation
- Fill in kruft: README_TEMPLATE.rst: Why use this?
- Fill in kruft: README_TEMPLATE.rst: Example usage
- Fill in kruft: README_TEMPLATE.rst: Author, copywrite
- Post-alpha: Fill in kruft: README_TEMPLATE.rst: Synopsis (After alpha-draft)
- Post-alpha: Test deployment into a seperate virtualenvironment (confirm requirements are correct)


Bugs
-----------
- Recursive loops occur when Union is used to instance/subclass check itself, and likely also when it is used on an inheritor (eg. isinstance(Union(NoneType, dict), Union))
