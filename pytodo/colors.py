"""color support for program output"""
#
# Copyright (C) 2006-2007 PyTodo Development Team
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# =============================================================================
# output colors, see:
# http://www.tldp.org/LDP/abs/html/colorizing.html#AEN15416
# http://sources.gentoo.org/viewcvs.py/portage/main/trunk/pym/portage/output.py
#
# Notice: this module doesn't show colors in win32
# =============================================================================

import os
import sys

# if windows disable colors
if os.name == 'nt':
	colorsEnabled = False
else:
	colorsEnabled = True

ESC = "\x1b["
ResetColor = ESC + "39;49;00m"
background = "01m"

colors = {
	"black" : "30",
	"red" : "31",
	"green" : "32",
	"yellow" : "33",
	"blue" : "34",
	"magenta" : "35",
	"cyan" : "36",
	"white" : "37"
	}

def colorize(ColorName, text):
	if not ColorName in colors.keys():
		raise "Invalid color name!"
	
	if colorsEnabled:
		setColor = ESC + colors[ColorName] + ';' + background
		return setColor + text + ResetColor
	else:
		return text

def test():
	print colorize("white", "If this text is white then everything is all right.")
	print colorize("green", "If this text is green then everything is all right.")
	print colorize("red", "If this text is red then everything is all right.")

if __name__ == "__main__":
	test()
