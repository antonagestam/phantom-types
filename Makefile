SHELL := /usr/bin/env bash

.PHONY: test
test:
	pytest

.PHONY: lint
lint:
	black --check .
	sorti --check .
	flake8
	mypy

.PHONY: format
format:
	sorti .
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
