# stdlib
from io import StringIO

# 3rd party
import coverage  # type: ignore
from coincidence.regressions import check_file_regression
from coverage.python import PythonParser  # type: ignore
from domdf_python_tools.paths import PathPlus
from pytest_regressions.file_regression import FileRegressionFixture

# this package
import coverage_pyver_pragma


def test_plugin(tmp_pathplus: PathPlus, file_regression: FileRegressionFixture):
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
	cov.erase()

	check_file_regression(output.getvalue().replace(tests.demo_code.__file__, "demo_code.py"), file_regression)
