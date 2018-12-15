"""
Environment Explorer V1 - 2018-12-15
By Andrew Hazelden <andrew@andrewhazelden.com>
----------------------------------------------
"""

from fx import *

def run():
	import fx
	import os
	
	print('\n\n---------------------------------------------------------------------------------')
	print('Environment Explorer')
	print('---------------------------------------------------------------------------------\n')
	
	# List all properties
	for env in os.environ:
		value = os.environ[env]
		print('\t[Env] ' + str(env) + '\t[Value] "' + value + '"')

# Create the action
class EnvironmentExplorerAction(Action):
	"""Explore Hook Properties."""
	
	def __init__(self):
		Action.__init__(self, 'Developer|Environment Explorer')
		
	def available(self):
		assert True
		
	def execute(self):
		run()

addAction(EnvironmentExplorerAction())
