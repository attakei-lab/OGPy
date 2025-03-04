from importlib import metadata

# Configuration file for the Sphinx documentation builder.
# -- Project information
project = "OGPy"
copyright = "2025, Kazuya Takei"
author = "Kazuya Takei"
release = metadata.version("ogpy")

# -- General configuration
extensions = [
    # Built-in extensions
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    # Third-party extensions
    # My extensions
    "ogpy.adapters.sphinx",
]
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for i18n
gettext_compact = False
locale_dirs = ["_locales"]

# -- Options for HTML output
html_title = f"{project} v{release}"
html_static_path = ["_static"]
html_theme = "bulma-basic"
html_theme_options = {
    "color_mode": "light",
    "bulmaswatch": "sandstone",
    "logo_description": "This is documentation of OGPy.",
    "sidebar_position": "right",
    "sidebar_size": 3,
    "navbar_icons": [
        {
            "label": "",
            "icon": "fa-brands fa-solid fa-github fa-2x",
            "url": "https://github.com/attakei-lab/OGPy",
        }
    ],
}
html_css_files = [
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/fontawesome.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/solid.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/brands.min.css",
    "main.css",
]
html_sidebars = {
    "**": [
        "sidebar/logo.html",
        "sidebar/line.html",
        "sidebar/searchbox.html",
        "sidebar/localtoc.html",
    ]
}

# -- Options for extensions
# sphinx.ext.intersphinx
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}
