====
OGPy
====

Modern consumer of `Open Graph protocol <https://ogp.me/>`_ for Python.

First goal
==========

The first purpose of this project is to provide new role and directive
that can translate to figure element form content URL with Open Graph protocol.

Example:

.. code:: rst

   .. ogp:image-link:: http://example.com

docutils handles it as this:

.. code:: rst

   .. figure:: http://example.com/OGP-IMAGE
      :target: http://example.com
      :alt: EXAMPLE.COM

      DESCRIPTION or TITLE

For implement these,
it provides simple consumer for ogp contents.
