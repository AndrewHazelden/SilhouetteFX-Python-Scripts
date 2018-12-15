"""
Node Explorer V1 - 2018-12-15
By Andrew Hazelden <andrew@andrewhazelden.com>
----------------------------------------------
"""

from fx import *

def run():
	import fx
	
	print('\n\n---------------------------------------------------------------------------------')
	print('Node Explorer')
	
	# Get the node selection
	sel = fx.selection()
	
	# Scan through all of the nodes
	for s in sel:
		print('\n---------------------------------------------------------------------------------\n')
		print('[Node] ' + str(s) + '\n')
		# List all properties
		for i in range(len(s.properties.keys())):
			key = s.properties.keys()[i]
			print('\t[Propery] ' + str(key) + ' [Value] "' + str(s.properties[key].value) + '"')


# Create the action
class NodeExplorerAction(Action):
	"""Explore Node Properties."""
	
	def __init__(self):
		Action.__init__(self, 'Developer|Node Explorer')
		
	def available(self):
		assert len(selection()) != 0, "Select a node."
		
	def execute(self):
		run()

addAction(NodeExplorerAction())