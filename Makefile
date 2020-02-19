SHELL := /usr/bin/env bash

clean:
	rm -rf dependent_types.egg-info __pycache__ build dist

build: clean
	python3 -m pip install --upgrade wheel twine setuptools
	python3 setup.py sdist bdist_wheel

distribute: build
	python3 -m twine upload dist/*

test-distribute: build
	python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

lint:
	flake8
	sorti --check .
	black --check .
	mypy .

test:
	pytest
