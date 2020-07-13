# stdlib
import platform
import sys

# this package
from coverage_pyver_pragma import PyVerPragmaPlugin, make_regexes, not_version_regex, regex_main


class MockConfig:

	def __init__(self):
		self.exclude_list = [regex_main]


def test_plugin():
	mock_config = MockConfig()
	PyVerPragmaPlugin().configure(mock_config)

	assert mock_config.exclude_list == [
			p.pattern for p in make_regexes(sys.version_info, platform.system(), platform.python_implementation())
			] + [not_version_regex]
