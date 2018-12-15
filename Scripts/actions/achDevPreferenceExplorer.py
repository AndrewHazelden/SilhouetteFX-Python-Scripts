"""
Preference Explorer V1 - 2018-12-15
By Andrew Hazelden <andrew@andrewhazelden.com>
----------------------------------------------
"""

from fx import *

def run():
	import fx
	
	print('\n\n---------------------------------------------------------------------------------')
	print('Preference Explorer')
	print('---------------------------------------------------------------------------------\n')
	
	# List all properties
	for i in range(len(prefs.keys())):
		key = prefs.keys()[i]
		print('\t[Pref] ' + str(key) + ' [Value] "' + str(fx.prefs[key]) + '"')

# Create the action
class PreferenceExplorerAction(Action):
	"""Explore Preference Properties."""
	
	def __init__(self):
		Action.__init__(self, 'Developer|Preference Explorer')
		
	def available(self):
		assert True
		
	def execute(self):
		run()

addAction(PreferenceExplorerAction())
