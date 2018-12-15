"""
Globals Explorer V1 - 2018-12-15
By Andrew Hazelden <andrew@andrewhazelden.com>
----------------------------------------------
"""

from fx import *

def run():
	import fx
	
	print('\n\n---------------------------------------------------------------------------------')
	print('Globals Explorer')
	print('---------------------------------------------------------------------------------\n')
	
	# List all properties
	for i in range(len(fx.globals.keys())):
		key = fx.globals.keys()[i]
		print('\t[Propery] ' + str(key) + ' [Value] "' + str(fx.globals.get(key)) + '"')

# Create the action
class GlobalsExplorerAction(Action):
	"""Explore Globals Properties."""
	
	def __init__(self):
		Action.__init__(self, 'Developer|Globals Explorer')
		
	def available(self):
		assert True
		
	def execute(self):
		run()

addAction(GlobalsExplorerAction())
