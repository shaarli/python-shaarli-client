Usage
=====

Once installed, ``shaarli-client`` provides the ``shaarli`` command,
which allows to interact with a Shaarli instance's REST API.

Getting help
------------

The ``-h`` and ``--help`` flags allow to display help for any command or sub-command:

.. code-block:: bash

   $ shaarli -h

   usage: shaarli [-h] [-u URL] [-s SECRET] [--output {json,pprint,text}]
                  {get-info,get-links} ...

   positional arguments:
     {get-info,get-links}  REST API endpoint
       get-info            Get information about this instance
       get-links           Get a collection of links ordered by creation date

   optional arguments:
     -h, --help            show this help message and exit
     -u URL, --url URL     Shaarli instance URL
     -s SECRET, --secret SECRET
                           API secret
     --output {json,pprint,text}
                           Output formatting


.. code-block:: bash

   $ shaarli get-links -h

   usage: shaarli get-links [-h] [--limit LIMIT] [--offset OFFSET]
                            [--searchtags SEARCHTAGS [SEARCHTAGS ...]]
                            [--searchterm SEARCHTERM [SEARCHTERM ...]]
                            [--visibility {all,private,public}]

   optional arguments:
     -h, --help            show this help message and exit
     --limit LIMIT         Number of links to retrieve or 'all'
     --offset OFFSET       Offset from which to start listing links
     --searchtags SEARCHTAGS [SEARCHTAGS ...]
                           List of tags
     --searchterm SEARCHTERM [SEARCHTERM ...]
                           Search terms across all links fields
     --visibility {all,private,public}
                           Filter links by visibility


Examples
--------

General syntax
~~~~~~~~~~~~~~

.. code-block:: bash

   $ shaarli <global arguments> <endpoint> <endpoint arguments>


GET info
~~~~~~~~

.. code-block:: bash

   $ shaarli -u https://host.tld/shaarli/ -s s3kr37 --output pprint get-info

   {
       "global_counter": 1502,
       "private_counter": 5,
       "settings": {
           "default_private_links": false,
           "enabled_plugins": [
               "markdown",
               "archiveorg"
           ],
           "header_link": "?",
           "timezone": "Europe/Paris",
           "title": "Yay!"
       }
   }


GET links
~~~~~~~~~

.. code-block:: bash

   $ shaarli -u https://host.tld/shaarli/ -s s3kr37 --output pprint get-links --searchtags super hero

   [
       {
           "created": "2015-02-22T15:14:41+00:00",
           "description": "",
           "id": 486,
           "private": false,
           "shorturl": null,
           "tags": [
               "wtf",
               "kitsch",
               "super",
               "hero",
               "spider",
               "man",
               "parody"
           ],
           "title": "Italian Spiderman",
           "updated": "2017-03-10T19:53:34+01:00",
           "url": "https://vimeo.com/42254051"
       },
       {
           "created": "2014-06-14T09:13:36+00:00",
           "description": "",
           "id": 970,
           "private": false,
           "shorturl": null,
           "tags": [
               "super",
               "hero",
               "comics",
               "spider",
               "man",
               "costume",
               "vintage"
           ],
           "title": "Here's Every Costume Spider-Man Has Ever Worn",
           "updated": "2017-03-10T19:53:34+01:00",
           "url": "http://mashable.com/2014/05/01/spider-man-costume"
       }
   ]
