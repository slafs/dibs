#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

tests_require = [
    'pytest',
    'pytest-django',
    'pytest-cov',
]


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name='dibs',
    version='0.1.0',
    description='make "dibs" on stuff',
    long_description=readme + '\n\n' + history,
    author='Slawek Ehlert',
    author_email='slafs@op.pl',
    url='https://github.com/slafs/dibs',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    install_requires=[],
    tests_require=tests_require,
    cmdclass={
        'test': PyTest,
    },
    license="MIT",
    zip_safe=False,
    keywords='dibs',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
)
