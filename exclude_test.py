# This file serves as a visual test that the conditional excludes are working correctly.

# stdlib
import sys

print("This line should be excluded on Windows")  # pragma: no cover (!Linux !Darwin)

print("This line should be excluded on Linux")  # pragma: no cover (!Windows !Darwin)

print("This line should be excluded on Darwin")  # pragma: no cover (!Windows !Linux)

print("This line should be excluded on Windows and Linux")  # pragma: no cover (!Darwin)

print("This line should be excluded on Windows and Darwin")  # pragma: no cover (!Linux)

print("This line should be excluded on Linux and Darwin")  # pragma: no cover (!Windows)

print("This line should be excluded on Python below 38")  # pragma: no cover (<Py38)

print("This line should be excluded on Python above 35")  # pragma: no cover (>=Py36)

print("This line should be excluded on Python above 35 on Windows and Darwin")  # pragma: no cover (>=Py36 !Linux)


def run():
	if sys.version_info < (3, 8):  # pragma: no cover (PY38+)

		for i in range(100):
			print(i)
	else:  # pragma: no cover (<PY38)
		for i in range(100, 200):
			print(i)


run()
