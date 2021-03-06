# stdlib
import sys

if sys.version_info < (3, 8):  # pragma: no cover (py38+)
	pass
elif sys.version_info[:2] == (3, 9):  # pragma: no cover (!py39)
	pass
else:  # pragma: no cover (<py38)
	pass
