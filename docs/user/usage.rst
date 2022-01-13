Usage
=====

Once installed, ``shaarli-client`` provides the ``shaarli`` command,
which allows to interact with a Shaarli instance's REST API.

Getting help
------------

The ``-h`` and ``--help`` flags allow to display help for any command or sub-command:

.. code-block:: bash

   $ shaarli -h

   usage: shaarli [-h] [-c CONFIG] [-i INSTANCE] [-u URL] [-s SECRET]
                  [-f {json,pprint,text}] [-o OUTFILE] [--insecure]
                  {get-info,get-links,post-link,put-link,get-tags,get-tag,put-tag,delete-tag,delete-link}
                  ...
   positional arguments:
     {get-info,get-links,post-link,put-link,get-tags,get-tag,put-tag,delete-tag,delete-link}
                           REST API endpoint
       get-info            Get information about this instance
       get-links           Get a collection of links ordered by creation date
       post-link           Create a new link or note
       put-link            Update an existing link or note
       get-tags            Get all tags
       get-tag             Get a single tag
       put-tag             Rename an existing tag
       delete-tag          Delete a tag from every link where it is used
       delete-link         Delete a link

   optional arguments:
     -h, --help            show this help message and exit
     -c CONFIG, --config CONFIG
                           Configuration file
     -i INSTANCE, --instance INSTANCE
                           Shaarli instance (configuration alias)
     -u URL, --url URL     Shaarli instance URL
     -s SECRET, --secret SECRET
                           API secret
     -f {json,pprint,text}, --format {json,pprint,text}
                           Output formatting
     -o OUTFILE, --outfile OUTFILE
                           File to save the program output to
     --insecure            Bypass API SSL/TLS certificate verification


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


.. note:: The following examples assume a :doc:`configuration` file is used

GET info
~~~~~~~~

.. code-block:: bash

   $ shaarli get-info


.. code-block:: json

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

   $ shaarli get-links --searchtags super hero


.. code-block:: json

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


POST link
~~~~~~~~~

.. code-block:: bash

   $ shaarli post-link --url https://w3c.github.io/activitypub/


.. code-block:: json

   {
       "created": "2018-06-04T20:35:12+00:00",
       "description": "",
       "id": 3252,
       "private": false,
       "shorturl": "kMkHHQ",
       "tags": [],
       "title": "https://w3c.github.io/activitypub/",
       "updated": "",
       "url": "https://w3c.github.io/activitypub/"
   }


PUT link
~~~~~~~~

.. code-block:: bash

   shaarli put-link --private 3252


.. code-block:: json

   {
       "created": "2018-06-04T20:35:12+00:00",
       "description": "",
       "id": 3252,
       "private": true,
       "shorturl": "kMkHHQ",
       "tags": [],
       "title": "?kMkHHQ",
       "updated": "2018-06-04T21:57:44+00:00",
       "url": "http://aaron.localdomain/~virtualtam/shaarli/?kMkHHQ"
   }


GET tags
~~~~~~~~

.. code-block:: bash

   $ shaarli get-tags --limit 5


.. code-block:: json

   [
       {
           "name": "bananas",
           "occurrences": 312
       },
       {
           "name": "snakes",
           "occurrences": 247
       },
       {
           "name": "ladders",
           "occurrences": 240
       },
       {
           "name": "submarines",
           "occurrences": 48
       },
       {
           "name": "yellow",
           "occurrences": 27
       }
   ]


GET tag
~~~~~~~

.. code-block:: bash

   $ shaarli get-tag bananas


.. code-block:: json

   {
       "name": "bananas",
       "occurrences": 312
   }


PUT tag
~~~~~~~

.. code-block:: bash

   $ shaarli put-tag w4c --name w3c


.. code-block:: json

   {
       "name": "w3c",
       "occurrences": 5
   }


New lines/line breaks
~~~~~~~~~~~~~~~~~~~~~

If you need to include line breaks in your descriptions, use a literal newline ``\n`` and **single quotes** around the description:

.. code-block:: bash

    $ shaarli post-link --url https://example.com/ --description 'One\nword\nper\nline'.


NOT (minus) operator
~~~~~~~~~~~~~~~~~~~~~

It is required to pass all values to `--searchtags` as a quoted string:

.. code-block:: bash

    $ shaarli get-links --searchtags "video -idontwantthistag"

The value passed to --searchtags must not start with a dash, a workaround is to start the string with a space:

.. code-block:: bash

    $ shaarli get-links --searchtags " -idontwantthistag -northisone"
