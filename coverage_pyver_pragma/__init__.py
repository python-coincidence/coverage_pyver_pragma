#!/usr/bin/env python3
#
#  __init__.py
"""
Plugin for Coverage.py to selectively ignore branches depending on the Python version.
"""
#
#  Copyright © 2020-2021 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
import re
from contextlib import suppress

# 3rd party
import coverage.python  # type: ignore
import pyparsing  # type: ignore
from coverage.config import DEFAULT_EXCLUDE  # type: ignore
from coverage.misc import join_regex  # type: ignore

# this package
from coverage_pyver_pragma.grammar import GRAMMAR

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2020-2021 Dominic Davis-Foster"
__license__: str = "MIT License"
__version__: str = "0.2.0"
__email__: str = "dominic@davis-foster.co.uk"

__all__ = ["DSL_EXCLUDE", "evaluate_exclude"]

DSL_EXCLUDE = re.compile(r'.*#\s*(?:pragma|PRAGMA)[:\s]?\s*(?:no|NO)\s*(?:cover|COVER)\s*\((.*)\)')
"""
Compiled regular expression to match comments in the ``# pragma: no cover (XXX)``,
where ``XXX`` is an expression to be evaluated to determine whether the line
should be excluded from coverage.

.. versionadded:: 0.2.0
"""


def evaluate_exclude(expression: str) -> bool:
	"""
	Evaluate the given expression to determine whether the line should be excluded from coverage.

	.. versionadded:: 0.2.0

	|

	:param expression:
	"""

	return all(list(GRAMMAR.parseString(expression.lower(), parseAll=True)))


class PythonParser(coverage.python.PythonParser):  # noqa: D102

	def lines_matching(self, *regexes):  # noqa: D102

		combined = join_regex([*regexes, *DEFAULT_EXCLUDE])

		regex_c = re.compile(combined)
		matches = set()

		for idx, ltext in enumerate(self.lines, start=1):

			dsl_m = DSL_EXCLUDE.match(ltext)

			# Check if it matches the DSL regex:
			if dsl_m:
				exclude_source = dsl_m.group(1)

				with suppress(pyparsing.ParseBaseException):
					if evaluate_exclude(exclude_source):
						matches.add(idx)
						continue

			if regex_c.search(ltext):
				matches.add(idx)

		return matches


def coverage_init(*args, **kwargs):
	coverage.python.PythonParser.lines_matching = PythonParser.lines_matching
