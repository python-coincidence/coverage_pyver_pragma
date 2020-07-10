# stdlib
import re
import sys
from typing import NamedTuple

# 3rd party
import pytest  # type: ignore

# this package
from coverage_pyver_pragma import PyVerPragmaPlugin, make_regexes, not_version_regex, regex_main

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
												test_string = f"{comment_string}{pragma_string}{post_pragma_space}{no_string}{post_no_space}{cover_string}{post_cover_space}({pre_version_sign}{py_string}{version}{post_version_sign})"
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


def test_correct_version_regex():
	py_3_versions = [
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
			]

	counter = 1

	post_version_sign = ''
	for python_version in py_3_versions:

		regexes = make_regexes(python_version)

		# TODO: Plus
		for pre_version_sign, minor_versions in zip(
			['>', '<', ">=", "<=", ''],
			[range(0, python_version.minor), range(python_version.minor + 1, 10), range(0, python_version.minor + 1), range(python_version.minor, 10), [python_version.minor], [python_version.minor]]
			):
			for minor_version in minor_versions:
				version = 30 + minor_version

				for comment_string in ['#', "# ", "#  ", "#\t", "# \t", "# \t ", "#\t "]:
					for pragma_string in ["pragma", "PRAGMA"]:
						for post_pragma_space in ['', ':', ": ", ":\t", "  "]:
							for no_string in ["no", "NO"]:
								for post_no_space in ['', ' ', '\t', "  "]:
									for cover_string in ["cover", "COVER"]:
										for post_cover_space in ['', ' ', '\t', "  "]:
											for py_string in ["Py", "PY", "py"]:
												# for post_version_sign in ['+', '']:

												test_string = f"{comment_string}{pragma_string}{post_pragma_space}{no_string}{post_no_space}{cover_string}{post_cover_space}({pre_version_sign}{py_string}{version}{post_version_sign})"  # print(f"[{counter} TESTING: {test_string}]")

												if not any([
														re.match(pattern.pattern, test_string)
														for pattern in regexes
														]):
													raise AssertionError(f"[{counter} FAIL: {test_string}]")
												counter += 1

	print(f"Ran {counter} tests")


class MockConfig:

	def __init__(self):
		self.exclude_list = [regex_main]


def test_plugin():
	mock_config = MockConfig()
	PyVerPragmaPlugin().configure(mock_config)

	assert mock_config.exclude_list == [p.pattern for p in make_regexes(sys.version_info)] + [not_version_regex]
