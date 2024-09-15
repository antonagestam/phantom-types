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
	pytest $(test)

.PHONY: test-runtime
test-runtime:
	pytest $(test) -k.py

.PHONY: test-typeguard
test-typeguard:
	pytest $(typeguard_arg) $(test)

.PHONY: test-typing
test-typing:
	pytest $(test) -k.yaml

.PHONY: clean
clean:
	rm -rf {**/,}*.egg-info **{/**,}/__pycache__ build dist .coverage coverage.xml

docs-requirements: export CUSTOM_COMPILE_COMMAND='make docs-requirements'
docs-requirements:
	@pip install --upgrade pip-tools
	@pip-compile
