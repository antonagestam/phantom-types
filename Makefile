SHELL := /usr/bin/env bash

.PHONY: test
test:
	pytest --ignore=examples --mypy-ini-file=setup.cfg $(test)

.PHONY: lint
lint:
	black --check .
	isort --check .
	flake8
	mypy

.PHONY: format-readme
format-readme:
	docker run --rm -v "$$PWD:/work" tmknom/prettier \
		--parser=markdown \
		--print-width=88 \
		--prose-wrap=always \
		--write \
		'**/*.md'

.PHONY: format
format:
	isort .
	black .

.PHONY: clean
clean:
	rm -rf *.egg-info **/__pycache__ build dist

.PHONY: build
build: clean
	python3 -m pip install --upgrade wheel twine setuptools
	python3 setup.py sdist bdist_wheel

.PHONY: distribute
distribute: build
	python3 -m twine upload dist/*

.PHONY: test-distribute
test-distribute: build
	python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
