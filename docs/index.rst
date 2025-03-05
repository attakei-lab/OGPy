====
Home
====

OGPy is Python 3-native implementation to consume for The Open Graph protocol.

It has purpose to provide dataset as :py:func:`dataclass <dataclasses.dataclass>` object from OGP metadata of html.

For use
=======

Installation
------------

This is published on attakei's private PyPI server.

.. code-block:: console

   pip install --extra-index=https://pypi.attakei.dev/simple/ OGPy

Usage guide
-----------

You can use it by some procedures.

* :doc:`console`
* :doc:`library`
* :doc:`/adapters/sphinx`

Notes
=====

This is ...
-----------

* Use features of python 3.
* Include some adapters.

This is not ...
---------------

* Do not keep compatibility for other OGP projects.
* Do not initiativity support integrations for other projects (work by my needs or explicitly desires)
* Do not support old python.

Motivation
----------

I (attakei) develop this to write reStructuredText directive
that generates image with link from content URL.
I need core feature of this to fetch metadata.


Sitemap
=======

.. toctree::
   :maxdepth: 2
   :includehidden:

   console
   library
   adapters/index
   api
   changes

