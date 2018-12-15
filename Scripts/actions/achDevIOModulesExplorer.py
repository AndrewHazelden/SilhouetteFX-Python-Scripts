"""
IO Modules Explorer V1 - 2018-12-15
By Andrew Hazelden <andrew@andrewhazelden.com>
----------------------------------------------
"""

from fx import *

def run():
	import fx
	
	print('\n\n---------------------------------------------------------------------------------')
	print('IO Modules Explorer')
	print('---------------------------------------------------------------------------------\n')

	# List all properties
	for i in range(len(fx.io_modules.keys())):
		key = fx.io_modules.keys()[i]
		print('\t[IO Module] ' + str(key))

# Create the action
class IOModulesExplorerAction(Action):
	"""Explore IO Modules Properties."""
	
	def __init__(self):
		Action.__init__(self, 'Developer|IO Modules Explorer')
		
	def available(self):
		assert True
		
	def execute(self):
		run()

addAction(IOModulesExplorerAction())
