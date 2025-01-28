from importlib import metadata

# Configuration file for the Sphinx documentation builder.
# -- Project information
project = "OGPy"
copyright = "2025, Kazuya Takei"
author = "Kazuya Takei"
release = metadata.version("ogpy")

# -- General configuration
extensions = [
    "sphinx.ext.autodoc",
    # My extensions
    "ogpy.adapter.sphinx",
]
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for i18n
gettext_compact = False
locale_dirs = ["_locales"]

# -- Options for HTML output
html_theme = "alabaster"
html_static_path = ["_static"]
