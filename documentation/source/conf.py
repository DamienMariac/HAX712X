# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

sys.path.insert(0, os.path.abspath('../code'))
print("sys.path:", sys.path)

project = 'BikeMap'
copyright = '2024, Damien Mariac, Abdoul-El Sawadogo, Julien Ollier, Marine Germain'
author = 'Damien Mariac, Abdoul-El Sawadogo, Julien Ollier, Marine Germain'
release = '1.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']
exclude_patterns = []
#html_static_path = ['_static']
html_baseurl = "https://damienmariac.github.io/HAX712X/"
language = 'fr'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'

autodoc_member_order = 'bysource'
