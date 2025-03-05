=============
Library usage
=============

This is usage with your Python applications.

Simple way
==========

:py:func:`ogpy.client.fetch` is useful function to generate Opengraph dataset object from URL.

.. code-block:: python
   :name: run.py

   from pprint import pprint
   from ogpy.client import fetch

   data = fetch("https://ogp.me")
   pprint(data)

.. code-block:: text
   :name: output-of-pprint

   Metadata(audio=None,
            description='The Open Graph protocol enables any web page to become a '
                        'rich object in a social graph.',
            determiner='',
            locale='en_US',
            locale_alternates=[],
            site_name=None,
            video=None,
            title='Open Graph protocol',
            type='website',
            url='https://ogp.me/',
            images=[ImageMetadata(url='https://ogp.me/logo.png',
                                  secure_url=None,
                                  type='image/png',
                                  width=300,
                                  height=300,
                                  alt='The Open Graph logo')])

:py:class:`ogpy.types.Metadata` is data class that has metadata of Opengraph from fetched content.
You access attribute of object to use in your works. (e.g. ``data.url`` )

Cache control
=============

Almost contents response itself with ``Cache-Control`` header.
OGPy provides function to return expired date with data object.

.. code-block:: python
   :name: run-with-cache.py

   from ogpy.client import fetch_for_cache

   data, age = fetch_for_cache("https://ogp.me")

:py:func:`ogpy.client.fetch_for_cache` returns tuple of data object and cachable age.
You can store data object until expire age if you need.

More information
================

See :doc:`/api`.
