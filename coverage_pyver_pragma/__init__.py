#!/usr/bin/env python3
#
#  __init__.py
"""
Plugin for Coverage.py to selectively ignore branches depending on the Python version.
"""
#
#  Copyright (c) 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

# stdlib
import re
import sys
from typing import List, NamedTuple, Pattern

# 3rd party
import coverage  # type: ignore

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2020 Dominic Davis-Foster"

__license__: str = "LGPLV3+"
__version__: str = "0.1.1"
__email__: str = "dominic@davis-foster.co.uk"

regex_main: str = re.compile(r"#\s*(pragma|PRAGMA)[:\s]?\s*(no|NO)\s*(cover|COVER)").pattern
not_version_regex: str = re.compile(fr"{regex_main}\s*((?!\(.{{0,2}}(py|PY|Py)3\d(\+)?\)).)*$").pattern


class Version(NamedTuple):
	major: int
	minor: int
	micro: int


def make_regexes(version_tuple: Version) -> List[Pattern]:
	if version_tuple.major == 3:
		# Python 3.X

		greater_than_versions = [str(x) for x in range(0, version_tuple.minor)]
		greater_equal_versions = [*greater_than_versions, str(version_tuple.minor)]
		less_than_versions = [str(x) for x in range(version_tuple.minor + 1, 10)]
		# Current max Python version is 3.9
		less_equal_versions = [str(version_tuple.minor), *less_than_versions]
		exact_versions = [str(version_tuple.minor)]

		# Add regular expressions for relevant python versions
		# We do it with re.compile to get the syntax highlighting in PyCharm
		excludes = [
				re.compile(fr"{regex_main}\s*\(<(py|PY|Py)3({'|'.join(less_than_versions)})\)"),
				re.compile(fr"{regex_main}\s*\(<=(py|PY|Py)3({'|'.join(less_equal_versions)})\)"),
				re.compile(fr"{regex_main}\s*\(>(py|PY|Py)3({'|'.join(greater_than_versions)})\)"),
				re.compile(fr"{regex_main}\s*\((py|PY|Py)3({'|'.join(greater_than_versions)})+\)"),
				re.compile(fr"{regex_main}\s*\(>=(py|PY|Py)3({'|'.join(greater_equal_versions)})\)"),
				re.compile(fr"{regex_main}\s*\((py|PY|Py)3({'|'.join(exact_versions)})\)"),
				]

		return excludes


class PyVerPragmaPlugin(coverage.CoveragePlugin):

	def configure(self, config):

		# Coverage.py gives either a Coverage() object, or a CoverageConfig() object.
		if isinstance(config, coverage.Coverage):
			config = config.config  # pragma: no cover

		# Remove standard "pragma: no cover" regex
		config.exclude_list.remove(regex_main)

		excludes = make_regexes(sys.version_info)
		for exc_pattern in excludes:
			config.exclude_list.append(exc_pattern.pattern)

		# print(config.exclude_list)

		# Reinstate the general regex, but making sure it isn't followed by a left bracket.
		config.exclude_list.append(not_version_regex)

		# TODO: Python 4.X


def coverage_init(reg, options):
	reg.add_configurer(PyVerPragmaPlugin())  # pragma: no cover
