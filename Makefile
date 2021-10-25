SHELL := /usr/bin/env bash

.PHONY: all

# Currently running typeguard on all modules except:
# - phantom.interval
# - phantom.base
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
	phantom.predicates.base \
	phantom.predicates.boolean \
	phantom.predicates.collection \
	phantom.predicates.datetime \
	phantom.prediactes.generic \
	phantom.predicates.interval \
	phantom.predicates.numeric \
	phantom.predicates.re \
	phantom.predicates.utils

pytest_args := \
	--mypy-ini-file=setup.cfg \
	--doctest-modules \
	--ignore=examples \
	--typeguard-packages=$(shell echo $(typeguard_packages) | sed 's/ /,/g')

.PHONY: test
test:
	pytest $(pytest_args) $(test)

.PHONY: test-runtime
test-runtime:
	pytest $(pytest_args) $(test) tests/{**/,}*.py

.PHONY: test-typing
test-typing:
	pytest $(pytest_args) $(test) tests/**{/*,}.yaml

.PHONY: coverage
coverage:
	@coverage run -m pytest $(pytest_args) $(test)

.PHONY: coverage-report
coverage-report:
	@coverage report
	@coverage xml

# TODO: Move to pre-commit
.PHONY: format-readme
format-readme:
	docker run \
		--rm \
		-v "$$PWD/README.md:/work/README.md" \
		tmknom/prettier \
		--parser=markdown \
		--print-width=88 \
		--prose-wrap=always \
		--write \
		'**/*.md'

.PHONY: clean
clean:
	rm -rf {**/,}*.egg-info **{/**,}/__pycache__ build dist .coverage coverage.xml
