=========
Syntax
=========

To ignore when running with versions of Python above, for instance, Python 3.6:

.. code-block:: python

	# pragma: no cover (>py36)

You can also ignore for a specific version of Python:

.. code-block:: python

	# pragma: no cover (py36)

Other examples:

.. code-block:: python

	# pragma: no cover (<py38)
	# pragma: no cover (<=py38)
	# pragma: no cover (>=py38)
	# pragma: no cover (py38+)


You can also exclude lines based on platform. For example, to exclude a line when the platform is not Windows:

.. code-block:: python

	# pragma: no cover (!Windows)

You can also exclude lines based on Python implementation. For example, to exclude a line when the implementation is not CPython:

.. code-block:: python

	# pragma: no cover (!CPython)

These can also be combined with the Python version:

.. code-block:: python

	# pragma: no cover (<=py36 !Windows !CPython)

This will ignore coverage (or lack thereof) for the branch if all three conditions are satisfied
(Python 3.6 or earlier AND not Windows AND not CPython).
It is not currently possible to ignore a branch if EITHER condition is true.
