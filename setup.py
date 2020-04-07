#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from importlib.machinery import SourceFileLoader
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))
VERSION = SourceFileLoader('', os.path.join(here, 'abeja', 'version.py')).load_module().VERSION


def _load_requires_from_file(filepath):
    return [pkg_name.rstrip('\r\n') for pkg_name in open(filepath).readlines()]


def _install_requires():
    requires = _load_requires_from_file('requirements.txt')
    return requires


if __name__ == '__main__':
    description = """
        ABEJA Platform Software Development Kit
    """
    setup(
        name='abeja-sdk',
        version=VERSION,
        description=description,
        author='ABEJA Inc.',
        author_email='platform-support@abejainc.com',
        packages=find_packages(exclude=["tests.*", "tests"]),
        install_requires=_install_requires(),
        include_package_data=True,
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Intended Audience :: Developers',
            'Topic :: Internet :: WWW/HTTP',
            'Operating System :: OS Independent',
        ]
    )
