# stdlib
import platform
import sys
from typing import Tuple, Type

# 3rd party
import pytest
from pyparsing import ParseBaseException  # type: ignore

# this package
from coverage_pyver_pragma import evaluate_exclude

platforms = {"Windows", "Linux", "Darwin", "Java"}
platforms.remove(platform.system())
platforms = {*platforms, *(p.lower() for p in platforms)}

versions = [(2, 7)]
versions.extend((3, v) for v in range(12))
versions.append((4, 0))

versions_before = versions[:versions.index(sys.version_info[:2])]
versions_after = versions[versions.index(sys.version_info[:2]):]
del versions

implementations = {"CPython", "PyPy", "Jython", "IronPython"}
implementations.remove(platform.python_implementation())
implementations = {*implementations, *(i.lower() for i in implementations)}


@pytest.mark.parametrize("implementation", implementations)
@pytest.mark.parametrize("plat", platforms)
@pytest.mark.parametrize("version", versions_before)
def test_grammar_dont_exclude(version: Tuple[int, int], implementation: str, plat: str):

	assert not evaluate_exclude(f"<py{version[0]}{version[1]} and {implementation} and {plat}")
	assert not evaluate_exclude(
			f"<py{version[0]}{version[1]} and not {platform.python_implementation()} and {plat}"
			)
	assert not evaluate_exclude(f"<py{version[0]}{version[1]} and ! {platform.python_implementation()} and {plat}")
	assert not evaluate_exclude(f"<py{version[0]}{version[1]} or not {implementation} and {plat}")
	assert not evaluate_exclude(f"<py{version[0]}{version[1]} or !{implementation} and {plat}")
	assert not evaluate_exclude(f"<py{version[0]}{version[1]}{implementation} and {plat}")

	assert not evaluate_exclude(f"<=py{version[0]}{version[1]}{implementation} and {plat}")
	assert not evaluate_exclude(f"<=py{version[0]}{version[1]}{implementation} or {plat}")
	assert not evaluate_exclude(f"<=py{version[0]}{version[1]}{implementation} and !{platform.system()}")
	assert not evaluate_exclude(f"py{version[0]}{version[1]}{implementation} and {plat}")
	assert not evaluate_exclude(f"py{version[0]}{version[1]}{implementation} or {plat}")


@pytest.mark.parametrize("plat", platforms)
@pytest.mark.parametrize("implementation", implementations)
@pytest.mark.parametrize("version", versions_after)
def test_grammar_exclude(version: Tuple[int, int], implementation: str, plat: str):

	assert evaluate_exclude(f"<=py{version[0]}{version[1]} and {platform.python_implementation()}")
	assert evaluate_exclude(f"<=py{version[0]}{version[1]} or {implementation}")
	assert evaluate_exclude(f"<=py{version[0]}{version[1]} or !{implementation} and not {plat}")
	assert evaluate_exclude(f"<=py{version[0]}{version[1]} or !{implementation} and {platform.system()}")


def test_grammar_current_platform_etc():
	version = sys.version_info
	assert evaluate_exclude(f"py{version[0]}{version[1]}")
	assert evaluate_exclude(f"<=py{version[0]}{version[1]}")
	assert evaluate_exclude(f">=py{version[0]}{version[1]}")
	assert evaluate_exclude(f"py{version[0]}{version[1]}+")

	assert evaluate_exclude(f"py{version[0]}{version[1]} {platform.python_implementation()}")
	assert evaluate_exclude(f"<=py{version[0]}{version[1]} {platform.python_implementation()}")
	assert evaluate_exclude(f">=py{version[0]}{version[1]} {platform.python_implementation()}")
	assert evaluate_exclude(f"py{version[0]}{version[1]}+ {platform.python_implementation()}")

	assert evaluate_exclude(f"py{version[0]}{version[1]} {platform.system()}")
	assert evaluate_exclude(f"<=py{version[0]}{version[1]} {platform.system()}")
	assert evaluate_exclude(f">=py{version[0]}{version[1]} {platform.system()}")
	assert evaluate_exclude(f"py{version[0]}{version[1]}+ {platform.system()}")

	assert evaluate_exclude(f"{platform.python_implementation()}")
	assert evaluate_exclude(f"{platform.system()}")


@pytest.mark.parametrize(
		"expression, exception",
		[
				("36", ParseBaseException),
				("36 and", ParseBaseException),
				("py36 and", ParseBaseException),
				("windows and", ParseBaseException),
				("!bpython and pypy", ParseBaseException),
				("<py38+", SyntaxError),
				]
		)
def test_bad_grammar(expression: str, exception: Type[Exception]):
	with pytest.raises(exception):
		evaluate_exclude(expression)


# TODO: tests for LogicalOp classes
