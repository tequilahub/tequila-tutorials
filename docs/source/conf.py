# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information


import os
import sys
# sys.path.insert(0, os.path.abspath('../source/code_to_document/'))  # Adjust if necessary
# sys.path.insert(0, 'source/')
sys.path.insert(0, os.path.abspath('../..'))
# os.path.abspath('..')

project = 'Tequila Documentation'
copyright = '2024, Ram Mosco'
author = 'Ram Mosco'
release = '13.9.2024'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
    'sphinx.ext.autodoc',
    'sphinxcontrib.programoutput', 
    'sphinx.ext.napoleon'  # Optional for Google/NumPy style docstrings
]

autosummary_generate = True


templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = 'alabaster'
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
