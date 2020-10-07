SHELL := /usr/bin/env bash

.PHONY: all test coverage coverage-report lint lint-makefile format-readme format \
		clean distribute test-distribute

test:
	pytest --ignore=examples --mypy-ini-file=setup.cfg $(test)

coverage:
	coverage run -m pytest --ignore=examples --mypy-ini-file=setup.cfg $(test)

coverage-report:
	@coverage report

lint:
	black --check .
	isort --check .
	flake8
	mypy

format-readme:
	docker run \
		--rm \
		-v "$$PWD:/work" \
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
	rm -rf *.egg-info **/__pycache__ build dist

build: clean
	python3 -m pip install --upgrade wheel twine setuptools
	python3 setup.py sdist bdist_wheel

distribute: build
	python3 -m twine upload dist/*

test-distribute: build
	python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
