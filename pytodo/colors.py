"""color support for program output"""
#
# Copyright (C) 2006 PyTodo Development Team
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
# =========================================================
# output colors, see:
# http://www.tldp.org/LDP/abs/html/colorizing.html#AEN15416
# or /usr/lib/portage/pym/output.py
#
# Notice: this module doesn't show colors in win32
# =========================================================

import os
import sys
#import output

class Colors:
	"""module for different colors in python"""
	
	ESC = "\x1b["
	ResetColor = ESC + "39;49;00m"
	#ResetColor = output.resetColor()
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

	background = "default"
	colorsEnabled = True
	
	def __init__(self):
		"""contructor"""
		self.checkOS()

	def setColor(self, ColorName, background = "01m"):
		"""set different color for output, while resetColor"""
		if self.colorsEnabled:
			selColor = self.ESC + self.colors[ColorName] + ';' + background
			sys.stdout.write(selColor)
	
	def resetColor(self): # unneeded!
		"""reset color to default"""
		if self.colorsEnabled:
			sys.stdout.write(self.ResetColor)
	
	def randomColor(self):
		"""random color - dont work"""
		pass
		
	def printc(self, string, color):
		"""print colored output and set color to default"""
		if self.colorsEnabled:
			self.setColor(color)
			print string + self.ResetColor
		else:
			print string
	
	def checkOS(self):
		"""check if os is windows"""
		if os.name == 'nt':
			self.colorsEnabled = False
		
def test1():
	x = Colors()
	x.printc("If this text is white then everything is all right.", "white")
	x.printc("If this text is green then everything is all right.", "green")
	x.printc("If this text is red then everything is all right.", "red")
	
#def test2():
#	print output.white("This text is white.")
#	print output.green("This text is green.")
#	print output.red("This text is red.")
				
if __name__ == "__main__":
	test1()
