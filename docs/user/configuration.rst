Configuration
=============

``shaarli-client`` loads information about Shaarli instances from a
configuration file, located at:

* ``~/.config/shaarli/client.ini`` (recommended)
* ``~/.shaarli_client.ini``
* ``shaarli_client.ini`` (in the current directory)
* user-specified location, using the ``-c``/``--config`` flag

Several Shaarli instances can be configured:

``[shaarli]``
   the default instance
``[shaarli:<my-other-instance>]``
   an additional instance that can be selected by passing the ``-i`` flag:
   ``$ shaarli -i my-other-instance get-info``

Example
-------

.. literalinclude:: client.ini
   :language: ini
