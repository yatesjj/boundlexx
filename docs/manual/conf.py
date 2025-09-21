# Configuration file for the Sphinx documentation builder.
# Boundlexx Master Manual Configuration

import os
import sys
from pathlib import Path

# -- Path setup --------------------------------------------------------------

# Add the project root to sys.path for autodoc
sys.path.insert(0, os.path.abspath('../../'))

# -- Project information -----------------------------------------------------

project = 'Boundlexx Master Manual'
copyright = '2025, Boundlexx Team'
author = 'Boundlexx Team'
version = '2025.1'
release = '2025.1.0'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'myst_parser',
    'sphinx_copybutton',
    'sphinx_design',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'canonical_url': '',
    'analytics_id': '',
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'vcs_pageview_mode': '',
    'style_nav_header_background': '#2980B9',
    # Toc options
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False
}

html_static_path = ['_static']
html_logo = None
html_favicon = None

# -- Options for MyST parser ------------------------------------------------

myst_enable_extensions = [
    "deflist",
    "tasklist",
    "html_admonition",
    "html_image",
    "colon_fence",
    "smartquotes",
    "replacements",
    "linkify",
    "strikethrough",
]

myst_heading_anchors = 3

# -- Options for todo extension ----------------------------------------------

todo_include_todos = True

# -- Options for intersphinx extension ---------------------------------------

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'django': ('https://docs.djangoproject.com/en/5.2/', 'https://docs.djangoproject.com/en/5.2/_objects/'),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}

# -- Options for copybutton extension ----------------------------------------

copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
copybutton_prompt_is_regexp = True

# -- Custom CSS and JS -------------------------------------------------------

html_css_files = [
    'custom.css',
]

html_js_files = [
    'custom.js',
]

# -- Autodoc configuration ---------------------------------------------------

autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__'
}
