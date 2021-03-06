#!/usr/bin/env python3
#
#  grammar.py
"""
.. versionadded:: 0.2.0

As with ``coverage.py``, lines are marked with comments in the form::

	# pragma: no cover

With ``coverage_pyver_pragma``, the comment may be followed with an expression enclosed in parentheses::

	# pragma: no cover (<=py38 and !Windows)

Each expression consists of one or more tags
(:py:data:`VERSION_TAG`, :py:data:`PLATFORM_TAG` or :py:data:`IMPLEMENTATION_TAG`).
The tags can be joined with the keywords ``AND``, ``OR`` and ``NOT``, with the exclamation mark ``!`` implying ``NOT``.
Parentheses can be used to group sub expressions.
A series of tags without keywords in between them are evaluated with ``AND``.

.. py:data:: VERSION_TAG

A ``VERSION_TAG`` comprises an optional comparator (one of ``<=``, ``<``, ``>=``, ``>``),
a version specifier in the form ``pyXX``, and an optional ``+`` to indicate ``>=``.

**Examples:**

.. parsed-literal::

	<=py36
	>=py37
	<py38
	>py27
	py34+  # equivalent to >=py34


.. py:data::  PLATFORM_TAG

A ``PLATFORM_TAG`` comprises a single word which will be compared (ignoring case)
with the output of :func:`platform.system`.

**Examples:**

.. parsed-literal::

	Windows
	Linux
	Darwin  # macOS
	Java

If the current platform cannot be determined all strings are treated as :py:obj:`True`.


.. py:data:: IMPLEMENTATION_TAG

An ``IMPLEMENTATION_TAG`` comprises a single word which will be compared (ignoring case)
with the output of :func:`platform.python_implementation`.

**Examples:**

.. parsed-literal::

	CPython
	PyPy
	IronPython
	Jython

Examples
-----------

ignore if the Python version is less than or equal to 3.7::

	# pragma: no cover (<=py37)

ignore if running on Python 3.9::

	# pragma: no cover (py39)

Ignore if the Python version is greater than 3.6 and it's not running on PyPy::

	# pragma: no cover (>py36 and !PyPy)

Ignore if the Python version is less than 3.8 and it's running on Windows::

	# pragma: no cover (Windows and <py38)

Ignore when not running on macOS (Darwin)::

	# pragma: no cover (!Darwin)

Ignore when not running on CPython::

	# pragma: no cover (!CPython)

API Reference
----------------

"""  # noqa: D400
#
#  Copyright © 2021 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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
import platform

# 3rd party
import packaging.specifiers
from domdf_python_tools.doctools import prettify_docstrings
from domdf_python_tools.stringlist import DelimitedList
from pyparsing import (  # type: ignore
		CaselessKeyword,
		CaselessLiteral,
		Combine,
		Group,
		Literal,
		OneOrMore,
		Optional,
		ParserElement,
		ParseResults,
		Word,
		infixNotation,
		nums,
		oneOf,
		opAssoc
		)

__all__ = [
		"ImplementationTag",
		"LogicalAND",
		"LogicalNOT",
		"LogicalOR",
		"LogicalOp",
		"PlatformTag",
		"VersionTag",
		"VERSION_TAG",
		"PLATFORM_TAG",
		"IMPLEMENTATION_TAG",
		"GRAMMAR",
		]


@prettify_docstrings
class VersionTag(packaging.specifiers.SpecifierSet):
	"""
	Represents a ``VERSION_TAG`` in the expression grammar.

	A ``VERSION_TAG`` comprises an optional comparator (one of ``<=``, ``<``, ``>=``, ``>``),
	a version specifier in the form ``pyXX``, and an optional ``+`` to indicate ``>=``.

	**Examples:**

	.. parsed-literal::

		<=py36
		>=py37
		<py38
		>py27
		py34+

	:param tokens:
	"""

	def __init__(self, tokens: ParseResults):
		token_dict = dict(tokens["version"])

		version = token_dict["version"][2:]

		if "plus" in token_dict and "comparator" in token_dict:
			raise SyntaxError("Cannot combine a comparator with the plus sign.")

		elif "plus" in token_dict:
			super().__init__(f">={version}")

		elif "comparator" in token_dict:
			comparator = token_dict["comparator"]
			super().__init__(f"{comparator}{version}")

		else:
			super().__init__(f"=={version}")

	def __repr__(self) -> str:  # pragma: no cover
		return f"<{self.__class__.__name__}({str(self)!r})>"

	def __bool__(self) -> bool:
		current_version = ''.join(platform.python_version_tuple()[:2])
		return current_version in self


@prettify_docstrings
class PlatformTag(str):
	"""
	Represents a ``PLATFORM_TAG`` in the expression grammar.

	A ``PLATFORM_TAG`` comprises a single word which will be compared (ignoring case)
	with the output of :func:`platform.system`.

	**Examples:**

	.. parsed-literal::

		Windows
		Linux
		Darwin  # macOS
		Java

	If the current platform cannot be determined all strings are treated as :py:obj:`True`.

	:param tokens:
	"""

	__slots__ = ()

	def __new__(cls, tokens: ParseResults):  # noqa: D102
		return super().__new__(cls, str(tokens["platform"]))

	def __repr__(self) -> str:  # pragma: no cover
		return f"<{self.__class__.__name__}({str(self)!r})>"

	def __bool__(self) -> bool:
		current_platform = platform.system().casefold()

		if not current_platform:  # pragma: no cover
			return True

		return current_platform == self.casefold()


@prettify_docstrings
class ImplementationTag(str):
	"""
	Represents an ``IMPLEMENTATION_TAG`` in the expression grammar.

	An ``IMPLEMENTATION_TAG`` comprises a single word which will be compared (ignoring case)
	with the output of :func:`platform.python_implementation`.

	**Examples:**

	.. parsed-literal::

		CPython
		PyPy
		IronPython
		Jython

	:param tokens:
	"""

	__slots__ = ()

	def __new__(cls, tokens: ParseResults):  # noqa: D102
		return super().__new__(cls, str(tokens["implementation"]))

	def __repr__(self) -> str:  # pragma: no cover
		return f"<{self.__class__.__name__}({str(self)!r})>"

	def __bool__(self) -> bool:
		return platform.python_implementation().casefold() == self.casefold()


@prettify_docstrings
class LogicalOp:
	"""
	Represents a logical operator (``AND``, ``OR``, and ``NOT / !``).

	:param tokens:
	"""

	def __init__(self, tokens: ParseResults):
		self.tokens = DelimitedList(tokens[0])

	def __format__(self, format_spec):
		return self.tokens.__format__(format_spec)

	def __getitem__(self, item):
		return self.tokens[item]

	def __str__(self) -> str:
		return f"[{self:, }]"

	def __repr__(self) -> str:  # pragma: no cover
		return f"<{self.__class__.__name__}({self})>"


@prettify_docstrings
class LogicalAND(LogicalOp):
	"""
	Represents the ``AND`` logical operator.

	:param tokens:
	"""

	def __bool__(self):
		return bool(self[0]) and bool(self[2])


@prettify_docstrings
class LogicalOR(LogicalOp):
	"""
	Represents the ``OR`` logical operator.

	:param tokens:
	"""

	def __bool__(self):
		return bool(self[0]) or bool(self[2])


@prettify_docstrings
class LogicalNOT(LogicalOp):
	"""
	Represents the ``NOT / !`` logical operator.

	:param tokens:
	"""

	def __bool__(self):
		return not bool(self[1])


# Logical operators
AND = CaselessKeyword("and")
OR = CaselessKeyword("or")
NOT = CaselessKeyword("not") | Literal('!')

# Grammar comprises (case insensitive):
# Python versions (<=pyXXX, pyXXX+)

PLUS = Literal('+').setResultsName("plus")

LESS_THAN_EQUAL = "<="
LESS_THAN = '<'
GREATER_THAN_EQUAL = ">="
GREATER_THAN = '>'

OPS = [LESS_THAN, LESS_THAN_EQUAL, GREATER_THAN, GREATER_THAN_EQUAL]
COMPARATOR = Optional(oneOf(' '.join(OPS))).setResultsName("comparator")

VERSION = Combine(CaselessLiteral("py") + Word(nums)).setResultsName("version")
VERSION_TAG = Group(COMPARATOR + VERSION + Optional(PLUS)).setResultsName("version")
VERSION_TAG.setParseAction(VersionTag)

# Platforms (Windows, !Linux)
# TODO: other platforms

WINDOWS = CaselessLiteral("windows")
LINUX = CaselessLiteral("linux")
DARWIN = CaselessLiteral("darwin")
JAVA = CaselessLiteral("java")

PLATFORM_TAG = (WINDOWS | LINUX | DARWIN | JAVA).setResultsName("platform")
PLATFORM_TAG.setParseAction(PlatformTag)

# Implementations (CPython, !PyPy)
# TODO: other python implementations

CPYTHON = CaselessLiteral("cpython")
PYPY = CaselessLiteral("pypy")
JYTHON = CaselessLiteral("jython")
IRONPYTHON = CaselessLiteral("ironpython")

IMPLEMENTATION_TAG = (CPYTHON | PYPY | JYTHON | IRONPYTHON).setResultsName("implementation")
IMPLEMENTATION_TAG.setParseAction(ImplementationTag)

ELEMENTS = VERSION_TAG | PLATFORM_TAG | IMPLEMENTATION_TAG

GRAMMAR: ParserElement = OneOrMore(
		infixNotation(
				ELEMENTS,
				[
						(NOT, 1, opAssoc.RIGHT, LogicalNOT),
						(AND, 2, opAssoc.LEFT, LogicalAND),
						(OR, 2, opAssoc.LEFT, LogicalOR),
						]
				)
		)
"""
The ``coverage_pyver_pragma`` expression grammar.

This can be used to parse an expression outside of the coverage context.
"""
