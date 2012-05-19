#!/usr/bin/env python

from distutils.core import setup
from pytodo.main import __version__
setup(
	name		= 'pytodo',
	version		= __version__,
	description	= 'script for managing todo list',
	author		= 'PoisoneR',
	author_email	= 'poisonerbg@gmail.com',
	url		= 'http://pytodo.openfmi.net',
	packages	= ['pytodo'],
	scripts		= ['bin/pytodo'],
	license		= 'GPL'
	)
