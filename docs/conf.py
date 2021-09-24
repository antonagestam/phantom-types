# This file only contains a selection of the most common options. For a full list see
# the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os
import pathlib
import sys

# If extensions (or modules to document with autodoc) are in another directory, add
# these directories to sys.path here. If the directory is relative to the documentation
# root, use os.path.abspath to make it absolute, like shown here.
sys.path.insert(0, os.path.abspath("../src"))

import phantom  # noqa: E402

current_dir = pathlib.Path(__file__).resolve().parent


def get_copyright_from_license() -> str:
    license = current_dir.parent / "LICENSE"
    prefix = "Copyright (c) "
    for line in license.read_text().split("\n"):
        if line.startswith(prefix):
            return line[len(prefix) :]
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
html_theme = "furo"
# Set typing.TYPE_CHECKING to True to enable "expensive" typing imports.
set_type_checking_flag = True
typehints_fully_qualified = True
always_document_param_types = True

# Add any paths that contain custom static files (such as style sheets) here, relative
# to this directory. They are copied after the builtin static files, so a file named
# "default.css" will overwrite the builtin "default.css".
# html_static_path = []

# Keep source order instead of sorting members alphabetically.
autodoc_member_order = "bysource"
