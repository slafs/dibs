#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

# Hack to prevent stupid "TypeError: 'NoneType' object is not callable" error
# in multiprocessing/util.py _exit_function when running `python
# setup.py test` (see
# http://www.eby-sarna.com/pipermail/peak/2010-May/003357.html)
for m in ('multiprocessing', 'billiard'):
    try:
        __import__(m)
    except ImportError:
        pass


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

tests_require = [
    'pytest',
    'pytest-django',
    'pytest-cov',
]


class PyTest(TestCommand):

    other_options = tuple()

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_args += self.other_options
        self.test_args += ['tests']
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

class PyTestCoverage(PyTest):

    other_options = ('--cov', 'dibs', '--cov-report', 'term-missing')


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
        'coverage': PyTestCoverage,
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
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    test_suite='tests',
)
