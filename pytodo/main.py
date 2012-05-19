#!/usr/bin/env python
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
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, 
# MA  02110-1301, USA.
#
# ==============================
# Todo
# sort by date
# find
# colors in option
# interactive menu
# pyqt or tk
# do not save pickle if started from __main__
# ==============================

import os
import sys
import getopt
import cPickle
from colors import Colors

__author__ = "PoisoneR"
__version__ = "0.1.4"
__copyright__ = "Copyright (C) 2006 PoisoneR <poisonerbg@gmail.com>"
__projecthome__ = "http://pytodo.openfmi.net"

class CTodoContainer:
	"""container with all CTodo's instances"""

	container = []
	savetodir = '~' + os.sep + '.pytodo'
	savetofile = 'todo'
	fileChanged = False

	def __init__(self):
		"""constructor load todo container"""
		self.savetodir = os.path.expanduser(self.savetodir)
		if (os.path.exists(self.savetodir + os.sep + self.savetofile)):
			fo = file(self.savetodir + os.sep + self.savetofile, 'r')
			CTodoContainer.container = cPickle.load(fo)
			fo.close()
		else:
			self.saveToFile()
	
	def __del__(self):
		"""destructor save file"""
		if (self.fileChanged):
			self.saveToFile()
	
	def saveToFile(self):
		"""self todo container in file"""
		self.sortByPriority()
		if not os.path.exists(self.savetodir):
			os.mkdir(self.savetodir, 0711)
		f = file(self.savetodir + os.sep + self.savetofile, 'w')
		cPickle.dump(CTodoContainer.container, f)
		f.close()
			
	
	def addTodo(self):
		"""add todo to container"""
		newCTodo = CTodo()
		newCTodo.add()
		CTodoContainer.container.append(newCTodo)
		self.fileChanged = True
	
	def viewTodos(self):
		"""show all todos"""
		color = Colors()
		color.printc('<<<<<<  ToDo List  >>>>>>','white')
		i = 0
		for todo in CTodoContainer.container:
			i = i + 1
			todo.view(i)
		color.printc('-------------------------','white')
	
	def deleteTodo(self, num):
		"""delete todo by number"""
		colors = Colors()
		ln = len(CTodoContainer.container)
		try:
			num = int(num)
		except ValueError:
			colors.printc('* You must enter integer value.', 'red')
		if num in range(1,  ln + 1):
			del(CTodoContainer.container[num - 1])
		else:
			colors.printc('* You must enter value in 1 to %s' % str(ln), 'red')
		self.fileChanged = True
			
	
	def sortByPriority(self):
		"""sort tod container by priority"""
		tmpContainer = []
		pr = 1
		while pr < 6:
			for todo in CTodoContainer.container:
				if todo.priority == pr:
					tmpContainer.append(todo)
			pr = pr + 1
		CTodoContainer.container = tmpContainer		




class CTodo:
	"""todo class"""
	
	#properties
	todoJob = ''
	priority = ''
	todate = ''
	
	def __init__(self):
		CTodo.allTodos = {} #to load from file
		
	def add(self):
		"""add todo"""
		colors = Colors()
		colors.printc("*Enter subject for to-do note.", "white")
		self.todoJob = raw_input('Subject: ')
		colors.printc("*Enter priority for the current note.", "white")
		colors.setColor("red")
		print "1. Highest"
		colors.setColor("yellow")
		print "2. High"
		colors.setColor("green")
		print "3. Medium"
		colors.setColor("cyan")
		print "4. Low"
		colors.setColor("blue")
		print "5. Lowest"
		colors.resetColor()
		msg = ''
		notInt = False
		while not notInt:
			try:
				if msg != '':
					colors.printc(msg, "red")
				
				self.priority = int(raw_input('Priority: '))
				notInt = True
			except ValueError:
				notInt = False
				msg = '* You must enter integer value.'
			if not self.priority in range(1,6):
				msg = '* You must enter digit from 1 to 5'
				notInt = False
		
		colors.printc("*Enter date to finish this job (optional)", "white")
		self.todate = raw_input('Due date: ')
		colors.resetColor()
		colors.printc('*You added successfully this todo "%s"' %
				self.todoJob, "white")

	def view(self, num = ''):
		"""show todo job"""
		colors = Colors()
		if self.priority == 1:
			color = "red"
		elif self.priority == 2:
			color = "yellow"
		elif self.priority == 3:
			color = "green"
		elif self.priority == 4:
			color = "cyan"
		elif self.priority == 5:
			color = "blue"
		else:
			color = "white"
		
		if num != '':
			if self.todate != '':
				colors.printc("%d. %s | Due date: %s" % (num,self.todoJob,self.todate), color)
			else:
				colors.printc("%d. %s" % (num,self.todoJob), color)
		else:
			colors.printc("%s to %s" % (self.todoJob,self.todate), color)

def errorPrint(errorMsg):
	"""print error message"""
	colors = Colors()
	colors.printc(errorMsg, "red")
	sys.exit(2)

def showLegend():
	"""legend with priority colors"""
	colors = Colors()
	colors.printc("<<< Priority Legend >>>", "white")
	print	
	colors.printc("* Highest", "red")
	colors.printc("* High", "yellow")
	colors.printc("* Medium", "green")
	colors.printc("* Low", "cyan")
	colors.printc("* Lowest", "blue")

def helpScreen():
	"""displays help messgage with options listing"""
	
	print '''Usage: pytodo [option] [argument]

Options:
  -a, --add		add todo job to the list
  -d, --del=NUM		delete todo job from the list
  -l, --list		list with all todo jobs
  -s, --showlegend	shows legend with priority colors
  -h, --help		prints this useful help message
  -m, --menu		show interactive menu
  -v, --version		show program's version'''

def verScreen():
	print 'PyTodo', __version__

def menuMode():
	print 'Not implemented!'

def parseOptions():
	tInst = CTodoContainer()
	if len(sys.argv) > 1:
		try:
			opts, args = getopt.getopt(sys.argv[1:], "hald:vms", ["help", "add","del=",
			"list", "help", "version", "menu", "showlegend"])
		except getopt.GetoptError:
			errorPrint('Wrong command-line option. See "pytodo --help" first.')
		#print opts
		#print args
		for option, argument in opts:
			if option in ['-a', '--add']:
				tInst.addTodo()
			if option in ['-d', '--del']:
				tInst.deleteTodo(argument)
			if option in ['-l', '--list']:
				tInst.viewTodos()
			if option in ['-h', '--help']:
				helpScreen()
			if option in ['-v', '--version']:
				verScreen()
			if option in ['-m', '--menu']:
				menuMode()
			if option in ['-s', '--showlegend']:
				showLegend()
	else:
		helpScreen()

def test():
	"""test"""
	print "<<< PyTodo started >>>"
	x = CTodoContainer()
	x.sortByPriority()
	x.viewTodos()
	print "<<< PyTodo finished >>>"

#if __name__=="__main__":
#	parseOptions()

# vim:set syntax=python:
