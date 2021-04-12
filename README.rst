######################
coverage_pyver_pragma
######################

.. start short_desc

**Plugin for Coverage.py to selectively ignore branches depending on the Python version.**

.. end short_desc


.. start shields

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	* - Docs
	  - |docs| |docs_check|
	* - Tests
	  - |actions_linux| |actions_windows| |actions_macos| |coveralls|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Anaconda
	  - |conda-version| |conda-platform|
	* - Activity
	  - |commits-latest| |commits-since| |maintained| |pypi-downloads|
	* - QA
	  - |codefactor| |actions_flake8| |actions_mypy|
	* - Other
	  - |license| |language| |requires|

.. |docs| image:: https://img.shields.io/readthedocs/coverage_pyver_pragma/latest?logo=read-the-docs
	:target: https://coverage_pyver_pragma.readthedocs.io/en/latest
	:alt: Documentation Build Status

.. |docs_check| image:: https://github.com/python-coincidence/coverage_pyver_pragma/workflows/Docs%20Check/badge.svg
	:target: https://github.com/python-coincidence/coverage_pyver_pragma/actions?query=workflow%3A%22Docs+Check%22
	:alt: Docs Check Status

.. |actions_linux| image:: https://github.com/python-coincidence/coverage_pyver_pragma/workflows/Linux/badge.svg
	:target: https://github.com/python-coincidence/coverage_pyver_pragma/actions?query=workflow%3A%22Linux%22
	:alt: Linux Test Status

.. |actions_windows| image:: https://github.com/python-coincidence/coverage_pyver_pragma/workflows/Windows/badge.svg
	:target: https://github.com/python-coincidence/coverage_pyver_pragma/actions?query=workflow%3A%22Windows%22
	:alt: Windows Test Status

.. |actions_macos| image:: https://github.com/python-coincidence/coverage_pyver_pragma/workflows/macOS/badge.svg
	:target: https://github.com/python-coincidence/coverage_pyver_pragma/actions?query=workflow%3A%22macOS%22
	:alt: macOS Test Status

.. |actions_flake8| image:: https://github.com/python-coincidence/coverage_pyver_pragma/workflows/Flake8/badge.svg
	:target: https://github.com/python-coincidence/coverage_pyver_pragma/actions?query=workflow%3A%22Flake8%22
	:alt: Flake8 Status

.. |actions_mypy| image:: https://github.com/python-coincidence/coverage_pyver_pragma/workflows/mypy/badge.svg
	:target: https://github.com/python-coincidence/coverage_pyver_pragma/actions?query=workflow%3A%22mypy%22
	:alt: mypy status

.. |requires| image:: https://requires.io/github/python-coincidence/coverage_pyver_pragma/requirements.svg?branch=master
	:target: https://requires.io/github/python-coincidence/coverage_pyver_pragma/requirements/?branch=master
	:alt: Requirements Status

.. |coveralls| image:: https://img.shields.io/coveralls/github/python-coincidence/coverage_pyver_pragma/master?logo=coveralls
	:target: https://coveralls.io/github/python-coincidence/coverage_pyver_pragma?branch=master
	:alt: Coverage

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/python-coincidence/coverage_pyver_pragma?logo=codefactor
	:target: https://www.codefactor.io/repository/github/python-coincidence/coverage_pyver_pragma
	:alt: CodeFactor Grade

.. |pypi-version| image:: https://img.shields.io/pypi/v/coverage_pyver_pragma
	:target: https://pypi.org/project/coverage_pyver_pragma/
	:alt: PyPI - Package Version

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/coverage_pyver_pragma?logo=python&logoColor=white
	:target: https://pypi.org/project/coverage_pyver_pragma/
	:alt: PyPI - Supported Python Versions

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/coverage_pyver_pragma
	:target: https://pypi.org/project/coverage_pyver_pragma/
	:alt: PyPI - Supported Implementations

.. |wheel| image:: https://img.shields.io/pypi/wheel/coverage_pyver_pragma
	:target: https://pypi.org/project/coverage_pyver_pragma/
	:alt: PyPI - Wheel

.. |conda-version| image:: https://img.shields.io/conda/v/domdfcoding/coverage_pyver_pragma?logo=anaconda
	:target: https://anaconda.org/domdfcoding/coverage_pyver_pragma
	:alt: Conda - Package Version

.. |conda-platform| image:: https://img.shields.io/conda/pn/domdfcoding/coverage_pyver_pragma?label=conda%7Cplatform
	:target: https://anaconda.org/domdfcoding/coverage_pyver_pragma
	:alt: Conda - Platform

.. |license| image:: https://img.shields.io/github/license/python-coincidence/coverage_pyver_pragma
	:target: https://github.com/python-coincidence/coverage_pyver_pragma/blob/master/LICENSE
	:alt: License

.. |language| image:: https://img.shields.io/github/languages/top/python-coincidence/coverage_pyver_pragma
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/python-coincidence/coverage_pyver_pragma/v0.3.0
	:target: https://github.com/python-coincidence/coverage_pyver_pragma/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/python-coincidence/coverage_pyver_pragma
	:target: https://github.com/python-coincidence/coverage_pyver_pragma/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2021
	:alt: Maintenance

.. |pypi-downloads| image:: https://img.shields.io/pypi/dm/coverage_pyver_pragma
	:target: https://pypi.org/project/coverage_pyver_pragma/
	:alt: PyPI - Downloads

.. end shields

Installation
--------------

.. start installation

``coverage_pyver_pragma`` can be installed from PyPI or Anaconda.

To install with ``pip``:

.. code-block:: bash

	$ python -m pip install coverage_pyver_pragma

To install with ``conda``:

	* First add the required channels

	.. code-block:: bash

		$ conda config --add channels http://conda.anaconda.org/conda-forge
		$ conda config --add channels http://conda.anaconda.org/domdfcoding

	* Then install

	.. code-block:: bash

		$ conda install coverage_pyver_pragma

.. end installation
