SHELL := /usr/bin/env bash

.PHONY: all

pytest_args = --mypy-ini-file=setup.cfg --doctest-modules --ignore=examples

.PHONY: test
test:
	pytest $(pytest_args) $(test)

.PHONY: test-runtime
test-runtime:
	pytest $(pytest_args) $(test) tests/**{/*,}.py

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

.PHONY: clean
clean:
	rm -rf {**/,}*.egg-info **{/**,}/__pycache__ build dist .coverage coverage.xml
