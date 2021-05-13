Change Log
==========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog`_ and this project adheres to
`Semantic Versioning`_.

.. _Keep A Changelog: http://keepachangelog.com/
.. _Semantic Versioning: http://semver.org/


`v0.4.1 <https://github.com/shaarli/python-shaarli-client/releases/tag/v0.4.1>`_ - 2021-05-13
---------------------------------------------------------------------------------------------

**Added:**

* Add support for Python 3.7, 3.8 and 3.9


**Changed:**

* Bump project and test requirements
* Update test tooling and documentation


**Removed:**

* Drop support for Python 3.4 and 3.5


**Security:**

* Rework JWT usage without the unmaintained requests-jwt library


`v0.4.0 <https://github.com/shaarli/python-shaarli-client/releases/tag/v0.4.0>`_ - 2020-01-09
---------------------------------------------------------------------------------------------

**Added:**

* CLI:

  * Add support for ``--insecure`` option (bypass SSL certificate verification)


`v0.3.0 <https://github.com/shaarli/python-shaarli-client/releases/tag/v0.3.0>`_ - 2019-02-23
---------------------------------------------------------------------------------------------

**Added:**

* CLI:

  * Add support for endpoint resource(s)

* REST API client:

  * ``PUT api/v1/links/<LINK_ID>``


**Fixed:**

* Use requests-jwt < 0.5
* Fix `POST /link` endpoint name


`v0.2.0 <https://github.com/shaarli/python-shaarli-client/releases/tag/v0.2.0>`_ - 2017-04-09
---------------------------------------------------------------------------------------------

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
