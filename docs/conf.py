# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full list see
# the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os
import pathlib
import sys

# If extensions (or modules to document with autodoc) are in another directory, add
# these directories to sys.path here. If the directory is relative to the documentation
# root, use os.path.abspath to make it absolute, like shown here.
sys.path.insert(0, os.path.abspath(".."))

import phantom

current_dir = pathlib.Path(__file__).resolve().parent


def get_copyright_from_license() -> str:
    license = current_dir.parent / "LICENSE"
    prefix = "Copyright (c) "
    for line in license.read_text().split("\n"):
        if line.startswith(prefix):
            return line.removeprefix(prefix)
    raise RuntimeError("Couldn't parse copyright from LICENSE")


# Project information
project = "phantom-types"
copyright = get_copyright_from_license()
author = "Anton Agestam"
version = phantom.__version__
release = version

# Add any Sphinx extension module names here, as strings. They can be extensions coming
# with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.viewcode",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
    "m2r2",
]  #

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and  directories to
# ignore when looking for source files. This pattern also affects html_static_path and
# html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# The theme to use for HTML and HTML Help pages.  See the documentation for a list of
# builtin themes.
html_theme = "sphinx_typlog_theme"
html_theme_options = {
    "logo_name": "phantom-types",
    "description": "Phantom types for Python",
    "github_user": "antonagestam",
    "github_repo": "phantom-types",
    "color": "#ff0089",
}

# Add any paths that contain custom static files (such as style sheets) here, relative
# to this directory. They are copied after the builtin static files, so a file named
# "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
