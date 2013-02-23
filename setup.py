#!/usr/bin/env python
# -*- coding: utf-8 -*-

# http://peak.telecommunity.com/DevCenter/setuptools#developer-s-guide
# from distutils.core import setup
from setuptools import setup, find_packages


def read_text(filename, dir=None):
    import codecs
    import os
    if dir is None:
        dir = os.path.abspath(os.path.dirname(__file__))
    filename = os.path.join(dir, filename)
    with codecs.open(filename, 'r', encoding='utf-8') as f:
        return f.read()

setup(
    url='https://github.com/nandoflorestan/python-dropbox-backup',
    name="poorbox",
    version='0.1dev',
    author='Nando Florestan',
    author_email="nandoflorestan@gmail.com",
    license='BSD',
    description="Downloads a dropbox directory via the dropbox REST API. "
        "Downloads only the changed files. Useful for environments without "
        "an X server.",
    long_description=read_text('README.rst'),
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite='tests',
    install_requires=['six', 'dropbox>=1.5.1'],  # argparse, 'bag>0.3'
    keywords=['dropbox', "python", 'REST', 'API', 'download', 'console'],
    classifiers=[  # http://pypi.python.org/pypi?:action=list_classifiers
        "Development Status :: 4 - Beta",
        # "Development Status :: 5 - Production/Stable",
        'Environment :: Console',
        "Environment :: No Input/Output (Daemon)",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators",
        'License :: OSI Approved :: BSD License',
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Topic :: Communications :: File Sharing",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Archiving :: Mirroring",
        "Topic :: System :: Software Distribution",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
        ],
    entry_points='''
[console_scripts]
poorbox = poorbox:main
''',
)
