SHELL := /usr/bin/env bash

.PHONY: all

# Currently running typeguard on all modules except:
# - phantom.interval
# - phantom._base
# - phantom.ext.phonenumbers
typeguard_packages := \
	phantom._hypothesis \
	phantom._utils.misc \
	phantom._utils.types \
	phantom._version \
	phantom.boolean \
	phantom.bounds \
	phantom.datetime \
	phantom.errors \
	phantom.fn \
	phantom.iso3166 \
	phantom.negated \
	phantom.re \
	phantom.schema \
	phantom.sized \
	phantom.predicates._base \
	phantom.predicates._utils \
	phantom.predicates.boolean \
	phantom.predicates.collection \
	phantom.predicates.datetime \
	phantom.prediactes.generic \
	phantom.predicates.interval \
	phantom.predicates.numeric \
	phantom.predicates.re
typeguard_arg := \
	--typeguard-packages=$(shell echo $(typeguard_packages) | sed 's/ /,/g')

tests_selection := 'external or not no_external'

.PHONY: test
test:
	pytest $(test) -m $(tests_selection)

.PHONY: test-runtime
test-runtime:
	pytest $(test) -k.py -m $(tests_selection)

.PHONY: test-typeguard
test-typeguard:
	pytest $(typeguard_arg) $(test) -k.py -m $(tests_selection)

.PHONY: test-typing
test-typing:
	pytest $(test) -k.yaml

.PHONY: clean
clean:
	rm -rf {**/,}*.egg-info **{/**,}/__pycache__ build dist .coverage coverage.xml

.PHONY: docs-requirements
docs-requirements: export CUSTOM_COMPILE_COMMAND='make docs-requirements'
docs-requirements:
	@pip install --upgrade pip-tools
	@pip-compile --output-file=docs-requirements.txt --extra=docs


.PHONY: docs-requirements
typing-requirements: export CUSTOM_COMPILE_COMMAND='make typing-requirements'
typing-requirements:
	@pip install --upgrade pip-tools
	@pip-compile --output-file=typing-requirements.txt --extra=type-check
