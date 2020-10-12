=============
Installation
=============

.. installation:: coverage_pyver_pragma
	:pypi:
	:github:
	:anaconda:
	:conda-channels: domdfcoding, conda-forge

Then enable the plugin in your coverage configuration.
The ``.coveragerc`` file in the repository root should contain the following options:

.. code-block:: ini

	[run]
	plugins =
	    coverage_pyver_pragma


Alternatively you can put the configuration in the ``setup.cfg`` or ``tox.ini`` files like so:

.. code-block:: ini

	[coverage:run]
	plugins =
	    coverage_pyver_pragma
