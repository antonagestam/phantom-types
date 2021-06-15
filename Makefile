SHELL := /usr/bin/env bash

.PHONY: all

pytest_args = --mypy-ini-file=setup.cfg --doctest-modules --ignore=examples

.PHONY: test
test:
	pytest $(pytest_args) $(test)

.PHONY: test-runtime
test-runtime:
	pytest $(pytest_args) $(test) tests/**{/*,}.py

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
	rm -rf *.egg-info **{/**,}/__pycache__ build dist .coverage
