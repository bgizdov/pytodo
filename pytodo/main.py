#!/usr/bin/env python
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

__author__ = "PoisoneR"
__version__ = "0.2.1"
__projecthome__ = "http://pytodo.openfmi.net"

import os
import sys
import getopt
from colors import colorize

if sys.version_info[:2] < (2, 5):
	try:
		import elementtree.ElementTree as ET
	except ImportError:
		print "ElementTree module not found! Please see INSTALL for help."
		sys.exit(1)
else:
	import xml.etree.ElementTree as ET

class CTodoContainer:
	"""container with all CTodo's instances"""

	container = []
	savetodir = '~' + os.sep + '.pytodo'
	savetofile = 'todos.xml'
	fileChanged = False

	def __init__(self):
		"""constructor for loading todo container from file"""
		self.savetodir = os.path.expanduser(self.savetodir)
		if (os.path.exists(self.savetodir + os.sep + self.savetofile)):
			#f = file(self.savetodir + os.sep + self.savetofile, 'r')
			#CTodoContainer.container = cPickle.load(f)
			#f.close()
			tree = ET.parse(self.savetodir + os.sep + self.savetofile)
			root = tree.getroot()
			for node in root:
				newCTodo = CTodo()
				newCTodo.todoJob = node.findtext("subject")
				newCTodo.priority = int(node.findtext("priority"))
				newCTodo.todate = node.findtext("date")
				CTodoContainer.container.append(newCTodo)

		else:
			self.firstRun()
	
	def __del__(self):
		"""destructor for saving file if changed"""
		if (self.fileChanged):
			self.saveToFile()

	def firstRun(self):
		"""run this function for the first time"""
		if not os.path.exists(self.savetodir):
			os.mkdir(self.savetodir, 0755)
		# Generate empty xml file
		root = ET.Element("pytodo")
		tree = ET.ElementTree(root)
		tree.write(self.savetodir + os.sep + self.savetofile)

	def indent(self, elem, level=0):
		"""indents a tree with each node according to its depth"""
		i = "\n" + level*"  "
		if len(elem):
			if not elem.text or not elem.text.strip():
				elem.text = i + "  "
			for elem in elem:
				self.indent(elem, level+1)
			if not elem.tail or not elem.tail.strip():
				elem.tail = i
		else:
			if level and (not elem.tail or not elem.tail.strip()):
				elem.tail = i
	    
	def saveToFile(self):
		"""self todo container in file"""
		self.sortByPriority()
		#f = file(self.savetodir + os.sep + self.savetofile, 'w')
		#cPickle.dump(CTodoContainer.container, f)
		#f.close()
		root = ET.Element("pytodo")
		for todo in CTodoContainer.container:
			entry = ET.SubElement(root, 'entry')
			subject = ET.SubElement(entry, 'subject')
			subject.text = todo.todoJob
			priority = ET.SubElement(entry, 'priority')
			priority.text = str(todo.priority)
			date = ET.SubElement(entry, 'date')
			date.text = todo.todate
		self.indent(root)
		tree = ET.ElementTree(root)
		tree.write(self.savetodir + os.sep + self.savetofile)
	
	def addTodo(self):
		"""add todo to container"""
		newCTodo = CTodo()
		newCTodo.add()
		CTodoContainer.container.append(newCTodo)
		self.fileChanged = True
	
	def viewTodos(self):
		"""show all todos"""
		print colorize('white', '<<<<<<  ToDo List  >>>>>>')
		i = 0
		for todo in CTodoContainer.container:
			i = i + 1
			todo.view(i)
		print colorize('white', '-------------------------')
	
	def deleteTodo(self, num):
		"""delete todo by number"""
		length = len(CTodoContainer.container)
		try:
			num = int(num)
		except ValueError:
			print colorize('red', '* You must enter integer value.')
		if num in range(1,  length + 1):
			del(CTodoContainer.container[num - 1])
		else:
			print colorize('red', '* You must enter value in 1 to %s' % str(length))
		self.fileChanged = True
			
	
	def sortByPriority(self):
		"""sort todo container by priority"""
		tmpContainer = []
		pri = 1
		while pri < 6:
			for todo in CTodoContainer.container:
				if todo.priority == pri:
					tmpContainer.append(todo)
			pri = pri + 1
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
		print colorize("white", ">> Enter subject for todo note")
		self.todoJob = raw_input('Subject: ')
		print colorize("white", ">> Enter priority for the current note")
		print colorize("red", "1. Highest")
		print colorize("yellow", "2. High")
		print colorize("green", "3. Medium")
		print colorize("cyan", "4. Low")
		print colorize("blue", "5. Lowest")

		msg = ''
		notInt = False
		while not notInt:
			try:
				if msg != '':
					print colorize("red", msg)
				self.priority = int(raw_input('Priority: '))
				notInt = True
			except ValueError:
				notInt = False
				msg = '[!] You must enter integer value'
			if not self.priority in range(1,6):
				msg = '[!] You must enter digit from 1 to 5'
				notInt = False
		
		print colorize("white", ">> Enter date to finish this job (optional)")
		self.todate = raw_input('Due date: ')
		print colorize("white", '>> You added successfully this todo "%s"' % self.todoJob)

	def view(self, num = ''):
		"""show todo job"""
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
				print colorize(color, "%d. %s | Due date: %s" % (num,self.todoJob, self.todate))
			else:
				print colorize(color, "%d. %s" % (num, self.todoJob))
		else:
			print colorize(color, "%s to %s" % (self.todoJob, self.todate))

def errorPrint(errorMsg):
	"""print error message"""
	print colorize("red", errorMsg)
	sys.exit(1)

def showLegend():
	"""legend with priority colors"""
	print colorize("white", "<<< Priority Legend >>>",)
	print
	print colorize("red", "* Highest",)
	print colorize("yellow", "* High")
	print colorize("green", "* Medium")
	print colorize("cyan", "* Low")
	print colorize("blue", "* Lowest")

def helpScreen():
	"""displays help messgage with options listing"""
	
	print '''Usage: pytodo [option] [argument]

Options:
  -a, --add		add todo job to the list
  -d, --del=NUM		delete todo job from the list
  -l, --list		list with all todo jobs
  -s, --showlegend	shows legend with priority colors
  -h, --help		show this useful help message and exit
  -m, --menu		show interactive menu
  -v, --version		show PyTodo version and exit'''

def verScreen():
	"""displays version"""
	print 'PyTodo', __version__

def menuMode():
	"""runs in interactive menu mode"""
	print 'Not implemented!'

def parseOptions():
	"""parses command line arguments"""
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

if __name__ == "__main__":
	parseOptions()
