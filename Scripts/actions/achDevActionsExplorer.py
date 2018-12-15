"""
Actions Explorer V1 - 2018-12-15
By Andrew Hazelden <andrew@andrewhazelden.com>
----------------------------------------------
"""

from fx import *

def run():
	import fx
	
	print('\n\n---------------------------------------------------------------------------------')
	print('Actions Explorer')
	print('---------------------------------------------------------------------------------\n')

	# List all properties
	for i in range(len(fx.actions.keys())):
		key = fx.actions.keys()[i]
		print('\t[Action] ' + str(key))
		
		# Extra action attributes
		# print(fx.Action(key).label)
		# print(fx.Action(key).id)

# Create the action
class ActionsExplorerAction(Action):
	"""Explore Actions Properties."""
	
	def __init__(self):
		Action.__init__(self, 'Developer|Actions Explorer')
		
	def available(self):
		assert True
		
	def execute(self):
		run()

addAction(ActionsExplorerAction())
