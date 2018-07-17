Installation
============

``shaarli-client`` is compatible with `Python <https://www.python.org/>`_ 3.4
and above and has been tested on Linux.

From the Python Package Index (PyPI)
------------------------------------

The preferred way of installing ``shaarli-client`` is within a Python `virtualenv`_;
you might want to use a wrapper such as `virtualenvwrapper`_ or `pew`_ for convenience.

.. _virtualenv: http://docs.python-guide.org/en/latest/dev/virtualenvs/
.. _virtualenvwrapper: https://virtualenvwrapper.readthedocs.io/en/latest/
.. _pew: https://github.com/berdario/pew

Here is an example using a Python 3.5 interpreter:

.. code-block:: bash

  # create a new 'shaarli' virtualenv
  $ python3 -m venv ~/.virtualenvs/shaarli

  # activate the 'shaarli' virtualenv
  $ source ~/.virtualenvs/shaarli/bin/activate

  # install shaarli-client
  (shaarli) $ pip install shaarli-client

  # check which packages have been installed
  $ pip freeze
  PyJWT==1.4.2
  requests==2.13.0
  requests-jwt==0.4
  shaarli-client==0.1.0

From the source code
--------------------

To get ``shaarli-client`` sources and install it in a new `virtualenv`_:

.. code-block:: bash

  # fetch the sources
  $ git clone https://github.com/shaarli/python-shaarli-client
  $ cd python-shaarli-client

  # create and activate a new 'shaarli' virtualenv
  $ python3 -m venv ~/.virtualenvs/shaarli
  $ source ~/.virtualenvs/shaarli/bin/activate

  # build and install shaarli-client
  (shaarli) $ python setup.py install

  # check which packages have been installed
  $ pip freeze
  PyJWT==1.4.2
  requests==2.13.0
  requests-jwt==0.4
  shaarli-client==0.1.0
