SHELL := /usr/bin/env bash

.PHONY: all

# Currently running typeguard on all modules except:
# - phantom.interval
# - phantom._base
# - phantom.ext.phonenumbers
typeguard_packages := \
	phantom.boolean \
	phantom.datetime \
	phantom.fn \
	phantom.iso3166 \
	phantom.re \
	phantom.schema \
	phantom.sized \
	phantom.utils \
	phantom.predicates._base \
	phantom.predicates.boolean \
	phantom.predicates.collection \
	phantom.predicates.datetime \
	phantom.prediactes.generic \
	phantom.predicates.interval \
	phantom.predicates.numeric \
	phantom.predicates.re \
	phantom.predicates.utils
typeguard_arg := \
	--typeguard-packages=$(shell echo $(typeguard_packages) | sed 's/ /,/g')

.PHONY: test
test:
	pytest $(test)  -m 'not no_external'

.PHONY: test-runtime
test-runtime:
	pytest $(test) -k.py -m 'not no_external'

.PHONY: test-typeguard
test-typeguard:
	pytest $(typeguard_arg) $(test)

.PHONY: test-typing
test-typing:
	pytest $(test) -k.yaml

.PHONY: clean
clean:
	rm -rf {**/,}*.egg-info **{/**,}/__pycache__ build dist .coverage coverage.xml

.PHONY: docs-requirements
docs-requirements: export UV_CUSTOM_COMPILE_COMMAND='make docs-requirements'
docs-requirements:
	@uv pip compile --generate-hashes --strip-extras --extra=docs --upgrade --output-file=docs-requirements.txt pyproject.toml


.PHONY: docs-requirements
typing-requirements: export UV_CUSTOM_COMPILE_COMMAND='make typing-requirements'
typing-requirements:
	@uv pip compile --generate-hashes --strip-extras --extra=type-check --upgrade --output-file=typing-requirements.txt pyproject.toml
