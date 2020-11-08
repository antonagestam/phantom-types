SHELL := /usr/bin/env bash

.PHONY: all test coverage coverage-report lint lint-makefile format-readme format \
		clean distribute test-distribute

pytest_args = --mypy-ini-file=setup.cfg --doctest-modules --ignore=examples

test:
	pytest $(pytest_args) $(test)

coverage:
	@coverage run -m pytest $(pytest_args) $(test)

coverage-report:
	@coverage report
	@coverage xml

lint:
	black --check .
	isort --check .
	flake8
	mypy

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

format:
	isort .
	black .

clean:
	rm -rf *.egg-info **/__pycache__ build dist .coverage

build: clean
	python3 -m pip install --upgrade wheel twine setuptools
	python3 setup.py sdist bdist_wheel

distribute: build
	python3 -m twine upload dist/*

test-distribute: build
	python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
