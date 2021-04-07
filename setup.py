#!/usr/bin/env python3
"""Setup script for shaarli-client"""
import codecs
import os
import re

from setuptools import find_packages, setup


def get_long_description():
    """Reads the main README.rst to get the program's long description"""
    with codecs.open('README.rst', 'r', 'utf-8') as f_readme:
        return f_readme.read()


def get_package_metadata(attribute):
    """Reads metadata from the main package's __init__"""
    with open(os.path.join('shaarli_client', '__init__.py'), 'r') as f_init:
        return re.search(
            r'^__{attr}__\s*=\s*[\'"]([^\'"]*)[\'"]'.format(attr=attribute),
            f_init.read(), re.MULTILINE
        ).group(1)


setup(
    name=get_package_metadata('title'),
    version=get_package_metadata('version'),
    description=get_package_metadata('brief'),
    long_description=get_long_description(),
    author=get_package_metadata('author'),
    maintainer='VirtualTam',
    maintainer_email='virtualtam@flibidi.net',
    license='MIT',
    url='https://github.com/shaarli/python-shaarli-client',
    keywords='bookmark bookmarking shaarli social',
    packages=find_packages(exclude=['tests.*', 'tests']),
    entry_points={
        'console_scripts': [
            'shaarli = shaarli_client.main:main',
        ],
    },
    install_requires=[
        'requests >= 2.25',
        'pyjwt == 2.0.1'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Utilities',
    ]
)
