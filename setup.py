#!/usr/bin/env python

from distutils.core import setup
from pytodo.main import __version__
setup(
	name		= 'pytodo',
	version		= __version__,
	description	= 'program for managing todo lists',
	author		= 'PoisoneR',
	author_email	= 'poisonertmp@gmail.com',
	url		= 'http://pytodo.openfmi.net',
	packages	= ['pytodo'],
	scripts		= ['bin/pytodo'],
	license		= 'GPL'
	)
