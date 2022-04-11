# stdlib
import os
from io import StringIO

# 3rd party
import coverage  # type: ignore[import]
import pytest
from coincidence import only_version
from coincidence.regressions import check_file_regression
from coverage.python import PythonParser  # type: ignore[import]
from domdf_python_tools.paths import PathPlus
from pytest_regressions.file_regression import FileRegressionFixture

# this package
import coverage_pyver_pragma


@pytest.mark.parametrize(
		"version",
		[
				pytest.param("3.6", marks=only_version(3.6, "Output differs on each version.")),
				pytest.param("3.7", marks=only_version(3.7, "Output differs on each version.")),
				pytest.param("3.8", marks=only_version(3.8, "Output differs on each version.")),
				pytest.param("3.9", marks=only_version(3.9, "Output differs on each version.")),
				pytest.param("3.10", marks=only_version("3.10", "Output differs on each version.")),
				]
		)
def test_plugin(
		tmp_pathplus: PathPlus,
		file_regression: FileRegressionFixture,
		version: str,
		) -> None:
	coverage_pyver_pragma.coverage_init()

	assert PythonParser.lines_matching is coverage_pyver_pragma.PythonParser.lines_matching

	cov = coverage.Coverage()
	cov.start()

	# this package
	import tests.demo_code

	cov.stop()
	cov.save()

	output = StringIO()
	cov.report(morfs=[tests.demo_code.__file__], file=output)
	# cov.html_report(morfs=[tests.demo_code.__file__])
	cov.erase()

	buf = output.getvalue().replace(tests.demo_code.__file__, "demo_code.py")
	buf = buf.replace(os.path.sep, os.path.altsep or os.path.sep)
	check_file_regression(buf, file_regression)
