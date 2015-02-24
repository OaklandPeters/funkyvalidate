from setuptools import setup

setup(
    name='funkyvalidate',
    version=open('VERSION').read().strip(),
    author='Oakland John Peters',
    author_email='oakland.peters@gmail.com',

    description='Run-time type-validation and duck-typing functions.',
    long_description=open('README.rst').read(),
    url='https://github.com/OaklandPeters/funkyvalidate',
    license='MIT',

    packages=['funkyvalidate'],

    include_package_data=True,

    classifiers=[
        #'Development Status :: 2 - Pre-Alpha',
        #'Development Status :: 3 - Alpha',
        #'Development Status :: 4 - Beta',
        #'Development Status :: 5 - Production/Stable',
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython',

        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
        'Topic :: Utilities'
    ]
)
