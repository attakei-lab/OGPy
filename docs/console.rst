==================
Console-mode usage
==================

OGPy provides ``ogpy`` command to display content data.

.. code-block:: console

   $ ogpy https://ogp.me
   ## Basic metadata

   title: Open Graph protocol
   url:   https://ogp.me/
   type:  website
   image: 1 items
           - url:    https://ogp.me/logo.png
             alt:    The Open Graph logo
             width:  300
             height: 300

   ## Optional metadata

   description:      The Open Graph protocol enables any web page to become a rich object in a social graph.
   locale:           en_US

JSON format
===========

CLI can also JSON style output.
This is convenience to integrate for shell-pipeline.

.. code-block:: console

   $ ogpy --format=json https://ogp.me
   {"title": "Open Graph protocol", "type": "website", "url": "https://ogp.me/", "images": [{"url": "https://ogp.me/logo.png", "secure_url": null, "type": "image/png", "width": 300, "height": 300, "alt": "The Open Graph logo"}], "audio": null, "description": "The Open Graph protocol enables any web page to become a rich object in a social graph.", "determiner": "", "locale": "en_US", "locale_alternates": [], "site_name": null, "video": null}

