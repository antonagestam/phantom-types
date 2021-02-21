SHELL := /usr/bin/env bash

.PHONY: all

pytest_args = --mypy-ini-file=setup.cfg --doctest-modules --ignore=examples

.PHONY: test
test:
	pytest $(pytest_args) $(test)

.PHONY: coverage
coverage:
	@coverage run -m pytest $(pytest_args) $(test)

.PHONY: coverage-report
coverage-report:
	@coverage report
	@coverage xml

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
	rm -rf *.egg-info **/__pycache__ build dist .coverage

.PHONY: build
build: clean
	python3 -m pip install --upgrade wheel twine setuptools
	python3 setup.py sdist bdist_wheel

.PHONY: distribute
distribute: build
	python3 -m twine check --strict dist/*
	python3 -m twine upload dist/*

.PHONY: test-distribute
test-distribute: build
	python3 -m twine check --strict dist/*
	python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
