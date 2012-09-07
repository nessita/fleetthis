# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function

import os

from collections import defaultdict
from cStringIO import StringIO
from unittest import TestCase

import pep8

from mock import patch
from pyflakes.scripts.pyflakes import checkPath

import fleetthis.fleetcore


class PackagePep8TestCase(TestCase):

    maxDiff = None
    packages = []
    exclude = ['migrations']

    def message(self, text):
        self.errors.append(text)

    def setUp(self):
        self.errors = {}
        self.pep8style = pep8.StyleGuide(
            counters=defaultdict(int),
            doctest='',
            exclude=self.exclude,
            filename=['*.py'],
            ignore=[],
            messages=self.errors,
            repeat=True,
            select=[],
            show_pep8=False,
            show_source=False,
            max_line_length=79,
            quiet=0,
            statistics=False,
            testsuite='',
            verbose=0,
        )

    def test_all_code(self):
        for package in self.packages:
            self.pep8style.input_dir(os.path.dirname(package.__file__))
        self.assertEqual(self.pep8style.options.report.total_errors, 0)


class FleetCorePep8TestCase(PackagePep8TestCase):

    packages = [fleetthis.fleetcore]


class PyFlakesTestCase(TestCase):

    def test_pyflakes(self):
        stdout = StringIO()
        with patch('sys.stdout', stdout):
            for dirpath, dirnames, filenames in os.walk('src'):
                for filename in filenames:
                    if filename.endswith('.py'):
                        checkPath(os.path.join(dirpath, filename))

        errors = [line.strip() for line in stdout.getvalue().splitlines() if
                  line.strip()]

        if errors:
            self.fail('\n'.join(errors))
