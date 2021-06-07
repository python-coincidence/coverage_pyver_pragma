=================
Configuration
=================

.. versionadded:: 0.3.0

When using Coverage.py's `reporting commands <https://coverage.readthedocs.io/en/coverage-5.5/cmd.html?highlight=report#coverage-summary-coverage-report>`_
it may be desirable to generate a report for a different Python version / implementation / platform to the current one.
For instance, you are generating a report from a ``.coverage`` file produced on PyPy 3.6 on Windows, but you are running CPython 3.8 on Linux.

``coverage_pyver_pragma`` provides three environment variables which can be used to set the target version and platform.

.. envvar:: COV_PYTHON_VERSION

	Sets the Python version. Must be in the form :file:`{<major>}.{<minor>}`.

	Defaults to the output of :func:`'.'.join(platform.python_version_tuple()[:2]) <platform.python_version_tuple>`.

	:bold-title:`Example:`

	.. prompt:: bash

		COV_PYTHON_VERSION=3.6 coverage report

.. envvar:: COV_PLATFORM

	Sets the Python platform.
	Must be a string which matches the output of :func:`platform.system` on the desired platform.

	Defaults to the output of :func:`platform.system`.

	:bold-title:`Example:`

	.. prompt:: bash

		COV_PLATFORM=Windows coverage report

.. envvar:: COV_PYTHON_IMPLEMENTATION

	Sets the Python implementation.
	Must be a string which matches the output of
	:func:`platform.python_implementation` with the desired implementation.

	Defaults to the output of :func:`platform.python_implementation`.

	:bold-title:`Example:`

	.. prompt:: bash

		COV_PYTHON_IMPLEMENTATION=PyPy coverage report

If you generate your coverage reports through `tox <https://tox.readthedocs.io/en/latest/>`_
you should configure `passenv <https://tox.readthedocs.io/en/latest/config.html?highlight=setenv#conf-passenv>`_
to ensure the environment variables are passed through:

.. code-block:: ini

	[testenv]
	passenv =
	    COV_PYTHON_VERSION
	    COV_PLATFORM
	    COV_PYTHON_IMPLEMENTATION
