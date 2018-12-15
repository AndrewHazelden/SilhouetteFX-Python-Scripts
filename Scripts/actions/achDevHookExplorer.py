"""
Hook Explorer V1 - 2018-12-15
By Andrew Hazelden <andrew@andrewhazelden.com>
----------------------------------------------
"""

from fx import *

def run():
	import fx
	
	print('\n\n---------------------------------------------------------------------------------')
	print('Hook Explorer')
	print('---------------------------------------------------------------------------------\n')

	# List all properties
	for i in range(len(fx.hooks.keys())):
		key = fx.hooks.keys()[i]
		print('\t[Hook] ' + str(key))

# Create the action
class HookExplorerAction(Action):
	"""Explore Hook Properties."""
	
	def __init__(self):
		Action.__init__(self, 'Developer|Hook Explorer')
		
	def available(self):
		assert True
		
	def execute(self):
		run()

addAction(HookExplorerAction())
