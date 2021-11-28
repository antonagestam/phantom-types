SHELL := /usr/bin/env bash

.PHONY: all

.PHONY: test
test:
	pytest $(test)

.PHONY: test-runtime
test-runtime:
	pytest $(test) tests/**{/*,}.py

.PHONY: test-typing
test-typing:
	pytest $(test) tests/**{/*,}.yaml

.PHONY: coverage
coverage:
	@coverage run -m pytest $(test)

.PHONY: coverage-report
coverage-report:
	@coverage report
	@coverage xml

.PHONY: clean
clean:
	rm -rf {**/,}*.egg-info **{/**,}/__pycache__ build dist .coverage coverage.xml
