#!/usr/bin/env python3
"""Setup script for shaarli-client"""
import codecs

from setuptools import find_packages, setup


def get_long_description():
    """Reads the main README.rst to get the program's long description"""
    with codecs.open('README.rst', 'r', 'utf-8') as f_readme:
        return f_readme.read()


setup(
    name='shaarli-client',
    version='0.1',
    description='CLI to interact with a Shaarli instance',
    long_description=get_long_description(),
    author='The Shaarli Community',
    maintainer='VirtualTam',
    maintainer_email='virtualtam@flibidi.net',
    license='MIT',
    url='https://github.com/shaarli/python-shaarli-client',
    keywords='bookmark bookmarking shaarli social',
    packages=find_packages(exclude=['tests.*', 'tests']),
    install_requires=[],
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
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
    ]
)
