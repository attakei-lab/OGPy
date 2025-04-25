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
       "ogpy.adapters.sphinx",
   ]

Usage
=====

.. rst:directive:: ogp:image

   Fetch content from URL, and render image with link.

.. rst:directive:: ogp:figure

   Fetch content from URL, and render image with link.
   This directive inherit :rst:dir:`figure` instead of :rst:dir:`image`.

Configurations
==============

.. confval:: ogp_use_browser
   :type: bool
   :default: ``False``

   If this value is ``True``, extension runs as :ref:`browser-mode` when fetching metadata from websites.

.. confval:: ogp_browser_name
   :type: str
   :default: ``"chromium"``

   Settings for what browser does it use when :confval:`ogp_use_browser` is ``True``.

Demo
====

.. tab-set::
   :sync-group: demo

   .. tab-item:: Output
      :sync: output

      .. ogp:image:: https://github.com/attakei-lab/OGPy
         :scale: 50%
         :align: center

   .. tab-item:: Source
      :sync: source

      .. code-block:: rst

         .. ogp:image:: https://github.com/attakei-lab/OGPy
            :scale: 50%
            :align: center

.. tab-set::
   :sync-group: demo

   .. tab-item:: Output
      :sync: output

      .. ogp:image:: https://dev.to/attakei/hosting-presentation-on-read-the-docs-3lkc
         :width: 80%
         :align: center

   .. tab-item:: Source
      :sync: source

      .. code-block:: rst

         .. ogp:image:: https://dev.to/attakei/hosting-presentation-on-read-the-docs-3lkc
            :width: 80%
            :align: center

.. tab-set::
   :sync-group: demo

   .. tab-item:: Output
      :sync: output

      .. ogp:figure:: https://github.com/attakei-lab/OGPy
         :scale: 50%
         :align: center

   .. tab-item:: Source
      :sync: source

      .. code-block:: rst

         .. ogp:figure:: https://github.com/attakei-lab/OGPy
            :scale: 50%
            :align: center

.. tab-set::
   :sync-group: demo

   .. tab-item:: Output
      :sync: output

      .. ogp:figure:: https://dev.to/attakei/hosting-presentation-on-read-the-docs-3lkc
         :width: 80%
         :align: center

   .. tab-item:: Source
      :sync: source

      .. code-block:: rst

         .. ogp:figure:: https://dev.to/attakei/hosting-presentation-on-read-the-docs-3lkc
            :width: 80%
            :align: center
