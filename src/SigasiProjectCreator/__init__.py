import sys
from os.path import abspath, normcase, splitdrive, join
from pathlib import PurePath


def absnormpath(p):
	"""
	Get a normalized absolute version of given path.
	
	Normalizes case of drive letters on Windows, but not the complete path.
	"""
	drive, tail = splitdrive(abspath(p))
	return join(normcase(drive), tail)


def posixpath(p):
	"""Convert a path to POSIX style, also on Windows."""
	return PurePath(p).as_posix()


def abort_if_false(condition, message, code=5):
	"""User-facing equivalent of assert"""
	if not condition:
		print(message)
		sys.exit(code)
