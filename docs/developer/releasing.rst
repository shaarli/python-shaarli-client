Releasing
=========

Reference:

* `Python Packaging User Guide`_

  * `Packaging and Distributing Projects`_

* `TestPyPI Configuration`_

Environment and requirements
----------------------------

`twine`_ is used to register Python projects to `PyPI`_ and upload release artifacts:

* ``PKG-INFO``: project description and metadata defined in ``setup.py``
* ``sdist``: source distribution tarball
* ``wheel``: binary release that can be platform- and interpreter- dependent

Development libraries need to be installed to build the project and upload artifacts
(see :doc:`testing`):

.. code-block:: bash

   (shaarli) $ pip install -r requirements/dev.txt

PyPI and TestPyPI configuration
-------------------------------

.. danger::

   Once uploaded, artifacts cannot be overwritten. If something goes wrong while
   releasing artifacts, you will need to bump the release version code and issue
   a new release.

   It is safer to test the release process on `TestPyPI`_ first; it provides
   a sandbox to experiment with project registration and upload.

``~/.pypirc``
~~~~~~~~~~~~~

.. literalinclude:: pypirc
   :language: ini


Releasing ``shaarli-client``
----------------------------

Checklist
~~~~~~~~~

* install Python dependencies
* setup PyPI and TestPyPI:

  * create an account on both servers
  * edit ``~/.pypirc``
  * register the project on both servers

* get a :doc:`gpg` key to sign the artifacts
* double check project binaries and metadata
* tag the new release
* build and upload the release on TestPyPI
* build and upload the release on PyPI

.. tip::

   A ``Makefile`` is provided for convenience, and allows to build, sign
   and upload artifacts on both `PyPI`_ and `TestPyPI`_.

TestPyPI
~~~~~~~~

.. code-block:: bash

   (shaarli) $ export IDENTITY=<GPG key ID>
   (shaarli) $ make test_release

PyPI
~~~~

.. code-block:: bash

   (shaarli) $ export IDENTITY=<GPG key ID>
   (shaarli) $ make release


.. _Packaging and Distributing Projects: https://packaging.python.org/distributing/
.. _PyPI: https://pypi.python.org/pypi
.. _Python Packaging User Guide: https://packaging.python.org
.. _TestPyPI: https://testpypi.python.org/pypi
.. _TestPyPI Configuration: https://wiki.python.org/moin/TestPyPI
.. _twine: https://pypi.python.org/pypi/twine
