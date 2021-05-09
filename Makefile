SHELL := /usr/bin/env bash

.PHONY: all

typeguard_packages := \
	phantom.boolean \
	phantom.datetime \
	phantom.interval \
	phantom.re \
	phantom.sized \
	phantom.predicates.base \
	phantom.predicates.boolean \
	phantom.predicates.collection \
	phantom.predicates.datetime \
	phantom.prediactes.generic \
	phantom.predicates.interval \
	phantom.predicates.numeric \
	phantom.predicates.re \
	phantom.ext.iso3166

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
	pytest $(pytest_args) $(test) tests/**{/*,}.py

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
	rm -rf *.egg-info **{/**,}/__pycache__ build dist .coverage

.PHONY: build
build: clean
	python3 -m pip install --upgrade wheel setuptools
	python3 setup.py sdist bdist_wheel

.PHONY: create-release
create-release:
	(\
	  tag="rr/v$$(python3 -c 'import phantom; print(phantom.__version__)')";\
	  git tag "$$tag";\
	  git push origin "$$tag";\
	)
