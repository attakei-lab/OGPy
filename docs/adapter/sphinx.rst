==================
Sphinx integration
==================

OGPy provide Sphinx-extension for integration.

Set up
======

It requires Sphinx.

.. code-block:: python
   :name: conf.py

   extension = [
       ...,  # Other extensions
       "ogpy.adapter.sphinx",
   ]

Usage
=====

``ogp-image-link`` directive
----------------------------

Fetch content from URL, and render image with link.
See :ref:`demo`.

.. _demo:

Demo
====

Source:

.. code-block:: rst

   .. ogp-image-link:: https://dev.to/attakei/hosting-presentation-on-read-the-docs-3lkc

Output:

.. ogp-image-link:: https://dev.to/attakei/hosting-presentation-on-read-the-docs-3lkc
   :width: 90%
   :align: center
