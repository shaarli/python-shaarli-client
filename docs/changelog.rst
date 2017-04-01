Change Log
==========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog`_ and this project adheres to
`Semantic Versioning`_.

.. _Keep A Changelog: http://keepachangelog.com/
.. _Semantic Versioning: http://semver.org/

`v0.2.0 <https://github.com/shaarli/python-shaarli-client/releases/tag/v0.2.0>`_ - UNPUBLISHED
----------------------------------------------------------------------------------------------

**Added:**

* Add client parameter checks and error handling
* Read instance information from a configuration file
* REST API client:

  * ``POST api/v1/links``

**Changed:**

* CLI:

  * rename ``--output`` to ``--format``
  * default to 'pprint' output format
  * improve endpoint-specific parser argument generation
  * improve exception handling and logging


`v0.1.0 <https://github.com/shaarli/python-shaarli-client/releases/tag/v0.1.0>`_ - 2017-03-12
---------------------------------------------------------------------------------------------

**Added:**

* Python project structure
* Packaging metadata
* Code quality checking (lint)
* Test coverage
* Sphinx documentation:

  * user - installation, usage
  * developer - testing, releasing

* Makefile
* Tox configuration
* Travis CI configuration
* REST API client:

  * ``GET /api/v1/info``
  * ``GET /api/v1/links``
