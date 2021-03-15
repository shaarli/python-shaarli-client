Testing
=======

See also:

* :doc:`../user/installation`

Environment and requirements
----------------------------

`Tox`_ is used to manage test `virtualenvs`_, and is the only tool needed to run
static analysis and unitary tests, as it will create the appropriate testing
virtualenvs on-the-fly.

.. code-block:: bash

  (shaarli) $ pip install -r requirements/ci.txt


Nevertheless, in case you want to install *test*, *development* and *documentation*
dependencies, e.g. for editor integration or local debugging:

.. code-block:: bash

  (shaarli) $ pip install -r requirements/dev.txt

Tools
-----

The documentation is written in `reStructuredText`_, using the `Sphinx`_ generator.

Coding style is checked using tools provided by the `Python Code Quality Authority`_:

* `isort`_: check import ordering and formatting
* `pycodestyle`_: Python syntax and coding style (see `PEP8`_)
* `pydocstyle`_: docstring formatting (see `PEP257`_)
* `pylint`_: syntax checking using predefined heuristics

Tests are run using the `pytest`_ test framework/harness, with the following plugins:

* `pytest-pylint`_: `pylint`_ integration
* `pytest-cov`_: `coverage`_ integration

Running the tests
-----------------

To renew test virtualenvs, run all tests and generate the documentation:

.. code-block:: bash

   $ tox -r

To run specific tests without renewing the corresponding virtualenvs:

.. code-block:: bash

   $ tox -e py34 -e py36

To run specific tests and renew the corresponding virtualenv:

.. code-block:: bash

   $ tox -r py35

.. _coverage: https://coverage.readthedocs.io/en/latest/
.. _isort: https://github.com/timothycrosley/isort#readme
.. _PEP8: http://pep8.readthedocs.org
.. _PEP257: http://pep257.readthedocs.org
.. _pycodestyle: http://pycodestyle.pycqa.org/en/latest/
.. _pydocstyle: http://www.pydocstyle.org/en/latest/
.. _pylint: http://www.pylint.org/
.. _pytest: http://docs.pytest.org/en/latest/
.. _pytest-cov: https://pytest-cov.readthedocs.io/en/latest/
.. _pytest-pylint: https://github.com/carsongee/pytest-pylint
.. _Python Code Quality Authority: http://meta.pycqa.org/en/latest/
.. _reStructuredtext: http://www.sphinx-doc.org/en/stable/rest.html
.. _Sphinx: http://www.sphinx-doc.org/en/stable/
.. _Tox: http://tox.readthedocs.org/en/latest/
.. _virtualenvs: https://virtualenv.pypa.io/en/stable/
