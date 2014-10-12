.PHONY: clean-pyc clean-build docs

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "testall - run tests on every Python version with tox"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "release - package and upload a release"
	@echo "sdist - package"

clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info
	find src -name '*.egg-info' -type d -exec rm -rf {} +
	rm -fr *.egg

clean-pyc:
	find . -name '*.pyc' -type f -exec rm -f {} +
	find . -name '*.pyo' -type f -exec rm -f {} +
	find . -name '*~' -type f -exec rm -f {} +
	find . -name '__pycache__' -type d -exec rm -rf {} +

lint:
	tox -e lint

test:
	python setup.py test

test-all:
	tox

coverage:
	tox -e coverage

docs:
	rm -f docs/dibs.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ src/dibs src/dibs/migrations
	$(MAKE) -C docs clean
	DJANGO_SETTINGS_MODULE=dibs.conf.settings $(MAKE) -C docs html
	#open docs/_build/html/index.html

release: clean
	bumpversion --list release
	python setup.py sdist bdist_wheel upload
	bumpversion --list patch

sdist: clean
	python setup.py sdist
	ls -l dist
