# stdlib
import re
import sys
from typing import NamedTuple

# 3rd party
import pytest

# this package
from coverage_pyver_pragma import PyVerPragmaPlugin, make_regexes, not_version_regex

# regex_main = re.compile(r"#\s*(pragma|PRAGMA)[:\s]?\s*(no|NO)\s*(cover|COVER)").pattern
# not_version_regex = re.compile(fr"{regex_main}((?!\(.{{0,2}}(py|PY|Py)3\d(\+)?\)).)*$").pattern


def test_not_version_regex():
	counter = 1

	for comment_string in ['#', "# ", "#  ", "#\t", "# \t", "# \t ", "#\t "]:
		for pragma_string in ["pragma", "PRAGMA"]:
			for post_pragma_space in ['', ':', ": ", ":\t", "  "]:
				for no_string in ["no", "NO"]:
					for post_no_space in ['', ' ', "\t", "  "]:
						for cover_string in ["cover", "COVER"]:
							for post_cover_space in ['', ' ', "\t", "  "]:
								for pre_version_sign in ['>', '<', ">=", "<=", '']:
									for py_string in ["Py", "PY", "py"]:
										for version in [30, 31, 32, 33, 34, 35, 36, 37, 38, 39]:
											for post_version_sign in ['+', '']:
												for plat in [" Windows", " Darwin", " Linux", '']:
													test_string = f"{comment_string}{pragma_string}{post_pragma_space}{no_string}{post_no_space}{cover_string}{post_cover_space}({pre_version_sign}{py_string}{version}{post_version_sign}{plat})"
												# print(f"[{counter} TESTING: {test_string}]")

												if re.match(not_version_regex, test_string):
													raise AssertionError(f"[{counter} FAIL: {test_string}]")
												counter += 1

	for comment_string in ['#', "# ", "#  ", "#\t", "# \t", "# \t ", "#\t "]:
		for pragma_string in ["pragma", "PRAGMA"]:
			for post_pragma_space in ['', ':', ": ", ":\t", "  "]:
				for no_string in ["no", "NO"]:
					for post_no_space in ['', ' ', "\t", "  "]:
						for cover_string in ["cover", "COVER"]:
							for post_cover_space in ['', ' ', "\t", "  "]:
								for post_cover_text in ['', "abcdefg", "hello world"]:
									test_string = f"{comment_string}{pragma_string}{post_pragma_space}{no_string}{post_no_space}{cover_string}{post_cover_space}{post_cover_text}"
									# print(f"[{counter} TESTING: {test_string}]")

									if re.match(not_version_regex, test_string) is None:
										raise AssertionError(f"[{counter} FAIL: {test_string}]")
									counter += 1

	print(f"Ran {counter} tests")


class Version(NamedTuple):
	major: int
	minor: int

	def __int__(self):
		return (self.major * 10) + self.minor


@pytest.mark.parametrize("current_platform", ["Windows", "Darwin", "Linux"])
@pytest.mark.parametrize("current_implementation", ["CPython", "Jython", "IronPython", "PyPy"])
@pytest.mark.parametrize("python_version", [
		Version(3, 0),
		Version(3, 1),
		Version(3, 2),
		Version(3, 3),
		Version(3, 4),
		Version(3, 5),
		Version(3, 6),
		Version(3, 7),
		Version(3, 8),
		Version(3, 9)
		])
def test_platforms_regex_values(current_platform, current_implementation, python_version):
	post_version_sign = ''
	comment_string = "# "
	pragma_string = "pragma"
	post_pragma_space = " "
	no_string = "NO"
	post_no_space = ''
	cover_string = "cover"
	post_cover_space = " "

	regexes = make_regexes(python_version, current_platform, current_implementation)

	versions_list = [
			range(0, python_version.minor),
			range(python_version.minor + 1, 10),
			range(0, python_version.minor + 1),
			range(python_version.minor, 10),
			[python_version.minor],
			[python_version.minor],
			]

	ignore_platforms = [f" !{x}" for x in ["Windows", "Darwin", "Linux"] if x != current_platform] + ['']
	ignore_implementations = [f" !{x}" for x in ["CPython", "Jython", "IronPython", "PyPy"] if x != current_implementation] + ['']
	counter = 1

	for pre_version_sign, minor_versions in zip(['>', '<', ">=", "<=", ''], versions_list):
		for minor_version in minor_versions:
			version = 30 + minor_version
			for py_string in ["Py", "PY", "py"]:
				for impl in ignore_implementations:
					# for post_version_sign in ['+', '']:
					for plat in ignore_platforms:

						test_string = f"{comment_string}{pragma_string}{post_pragma_space}{no_string}{post_no_space}{cover_string}{post_cover_space}({pre_version_sign}{py_string}{version}{post_version_sign}{plat}{impl})"
						print(".", end='')
						sys.stdout.flush()
						# print(f"[{counter} TESTING: {test_string}]")

						if not any([
								re.match(pattern.pattern, test_string)
								for pattern in regexes
								]):
							raise AssertionError(f"[{counter} FAIL: {test_string}]")

						counter += 1

	print(f"Ran {counter} tests")


@pytest.mark.parametrize("current_platform", ["Linux"])
@pytest.mark.parametrize("current_implementation", ["CPython"])
@pytest.mark.parametrize("python_version", [
		Version(3, 6),
		Version(3, 7),
		Version(3, 8),
		Version(3, 9)
		])
@pytest.mark.parametrize("no_string", ["no", "NO"])
@pytest.mark.parametrize("space", ['', ' ', '\t', "  "])
@pytest.mark.parametrize("cover_string", ["cover", "COVER"])
@pytest.mark.parametrize("py_string", ["Py", "PY", "py"])
@pytest.mark.parametrize("pragma_string", ["pragma", "PRAGMA"])
def test_platforms_regex_structure(current_platform, current_implementation, python_version, no_string ,space, cover_string, py_string, pragma_string):
	post_version_sign = ''

	regexes = make_regexes(python_version, current_platform, current_implementation)

	versions_list = [
			range(0, python_version.minor),
			range(python_version.minor + 1, 10),
			range(0, python_version.minor + 1),
			range(python_version.minor, 10),
			[python_version.minor],
			[python_version.minor],
			]

	ignore_platforms = [f" !{x}" for x in ["Windows", "Darwin", "Linux"] if x != current_platform] + ['']
	ignore_implementations = [f" !{x}" for x in ["CPython", "Jython", "IronPython", "PyPy"] if x != current_implementation] + ['']
	counter = 1

	for pre_version_sign, minor_versions in zip(['>', '<', ">=", "<=", ''], versions_list):
		for minor_version in minor_versions:
			version = 30 + minor_version
			for py_string in ["Py", "PY", "py"]:
				for impl in ignore_implementations:
					# for post_version_sign in ['+', '']:
					for plat in ignore_platforms:

						test_string = f"#{space}{pragma_string}:{space}{no_string}{space}{cover_string}{space}({pre_version_sign}{py_string}{version}{post_version_sign}{plat}{impl})"
						print(".", end='')
						sys.stdout.flush()
						# print(f"[{counter} TESTING: {test_string}]")

						if not any([
								re.match(pattern.pattern, test_string)
								for pattern in regexes
								]):
							raise AssertionError(f"[{counter} FAIL: {test_string}]")

						counter += 1

	print(f"Ran {counter} tests")


@pytest.mark.parametrize("current_platform", ["Linux"])
@pytest.mark.parametrize("current_implementation", ["CPython"])
@pytest.mark.parametrize("python_version", [Version(3, 9)])
@pytest.mark.parametrize("post_pragma_space", ['', ':', ": ", ":\t", "  "])
@pytest.mark.parametrize("no_string", ["no"])
@pytest.mark.parametrize("post_no_space", ['', ' ', '\t', "  "])
@pytest.mark.parametrize("cover_string", ["cover"])
@pytest.mark.parametrize("post_cover_space", ['', ' ', '\t', "  "])
@pytest.mark.parametrize("py_string", ["PY"])
@pytest.mark.parametrize("pragma_string", ["pragma"])
@pytest.mark.parametrize("comment_string", ['#', "# ", "#  ", "#\t", "# \t", "# \t ", "#\t "])
def test_platforms_regex_spaces(current_platform, current_implementation, python_version, post_pragma_space, no_string ,post_no_space, cover_string, post_cover_space, py_string, pragma_string, comment_string):
	post_version_sign = ''

	regexes = make_regexes(python_version, current_platform, current_implementation)

	versions_list = [
			range(0, python_version.minor),
			range(python_version.minor + 1, 10),
			range(0, python_version.minor + 1),
			range(python_version.minor, 10),
			[python_version.minor],
			[python_version.minor],
			]

	ignore_platforms = [f" !{x}" for x in ["Windows", "Darwin", "Linux"] if x != current_platform] + ['']
	ignore_implementations = [f" !{x}" for x in ["CPython", "Jython", "IronPython", "PyPy"] if x != current_implementation] + ['']
	counter = 1

	for pre_version_sign, minor_versions in zip(['>', '<', ">=", "<=", ''], versions_list):
		for minor_version in minor_versions:
			version = 30 + minor_version
			for py_string in ["Py", "PY", "py"]:
				for impl in ignore_implementations:
					# for post_version_sign in ['+', '']:
					for plat in ignore_platforms:

						test_string = f"{comment_string}{pragma_string}{post_pragma_space}{no_string}{post_no_space}{cover_string}{post_cover_space}({pre_version_sign}{py_string}{version}{post_version_sign}{plat}{impl})"
						print(".", end='')
						sys.stdout.flush()
						# print(f"[{counter} TESTING: {test_string}]")

						if not any([
								re.match(pattern.pattern, test_string)
								for pattern in regexes
								]):
							raise AssertionError(f"[{counter} FAIL: {test_string}]")

						counter += 1

	print(f"Ran {counter} tests")


#
#
# @pytest.mark.parametrize("current_platform", ["Windows", "Darwin", "Linux"])
# @pytest.mark.parametrize("current_implementation", ["CPython", "Jython", "IronPython", "PyPy"])
# @pytest.mark.parametrize("python_version", [
# 		Version(3, 0),
# 		Version(3, 1),
# 		Version(3, 2),
# 		Version(3, 3),
# 		Version(3, 4),
# 		Version(3, 5),
# 		Version(3, 6),
# 		Version(3, 7),
# 		Version(3, 8),
# 		Version(3, 9)
# 		])
# @pytest.mark.parametrize("pragma_string", ["pragma", "PRAGMA"])
# @pytest.mark.parametrize("comment_string", ['#', "# ", "#  ", "#\t", "# \t", "# \t ", "#\t "])
# def test_correct_version_regex(current_platform, python_version, pragma_string, comment_string, current_implementation):
# 	# @pytest.mark.parametrize("post_pragma_space", ['', ':', ": ", ":\t", "  "])
# 	# @pytest.mark.parametrize("no_string", ["no", "NO"])
# 	# @pytest.mark.parametrize("post_no_space", ['', ' ', '\t', "  "])
# 	# @pytest.mark.parametrize("cover_string", ["cover", "COVER"])
# 	# @pytest.mark.parametrize("post_cover_space", ['', ' ', '\t', "  "])
# 	# @pytest.mark.parametrize("py_string", ["Py", "PY", "py"])
# 	counter = 1
#
# 	post_version_sign = ''
#
# 	regexes = make_regexes(python_version, current_platform, current_implementation)
#
# 	versions_list = [
# 			range(0, python_version.minor),
# 			range(python_version.minor + 1, 10),
# 			range(0, python_version.minor + 1),
# 			range(python_version.minor, 10),
# 			[python_version.minor],
# 			[python_version.minor],
# 			]
#
# 	ignore_platforms = [f" !{x}" for x in ["Windows", "Darwin", "Linux"] if x != current_platform] + ['']
# 	ignore_implementations = [f" !{x}" for x in ["CPython", "Jython", "IronPython", "PyPy"] if x != current_implementation] + ['']
#
# 	# TODO: Plus
# 	for pre_version_sign, minor_versions in zip(['>', '<', ">=", "<=", ''], versions_list):
# 		for minor_version in minor_versions:
# 			version = 30 + minor_version
#
# 			for post_pragma_space in ['', ':', ": ", ":\t", "  "]:
# 					for no_string in ["no", "NO"]:
# 						for post_no_space in ['', ' ', '\t', "  "]:
# 							for cover_string in ["cover", "COVER"]:
# 								for post_cover_space in ['', ' ', '\t', "  "]:
# 									for py_string in ["Py", "PY", "py"]:
# 										for impl in ignore_implementations:
# 											# for post_version_sign in ['+', '']:
# 											for plat in ignore_platforms:
#
# 												test_string = f"{comment_string}{pragma_string}{post_pragma_space}{no_string}{post_no_space}{cover_string}{post_cover_space}({pre_version_sign}{py_string}{version}{post_version_sign}{plat}{impl})"
# 												print(".", end='')
# 												sys.stdout.flush()
# 												# print(f"[{counter} TESTING: {test_string}]")
#
# 												if not any([
# 														re.match(pattern.pattern, test_string)
# 														for pattern in regexes
# 														]):
# 													raise AssertionError(f"[{counter} FAIL: {test_string}]")
# 												counter += 1
#
# 	print(f"Ran {counter} tests")


@pytest.mark.parametrize(
		"version_tuple",
		[
				Version(1, 0),
				Version(1, 1),
				Version(1, 2),
				Version(1, 3),
				Version(1, 4),
				Version(1, 6),
				Version(2, 0),
				Version(2, 1),
				Version(2, 2),
				Version(2, 3),
				Version(2, 4),
				Version(2, 5),
				Version(2, 6),
				Version(2, 7),
				Version(4, 0),
				Version(4, 1),
				Version(4, 2),
				Version(4, 3),
				Version(4, 4),
				Version(4, 5),
				Version(4, 6),
				Version(4, 7),
				Version(4, 8),
				Version(4, 9),
				]
		)
def test_invalid_versions(version_tuple):
	with pytest.raises(ValueError):
		make_regexes(version_tuple, "Linux", "CPython")
