

"""
Session Explorer V1 - 2018-12-15
By Andrew Hazelden <andrew@andrewhazelden.com>
----------------------------------------------
"""

from fx import *

def run():
	import fx
	
	print('\n\n---------------------------------------------------------------------------------')
	print('Session Explorer')
	print('---------------------------------------------------------------------------------\n')
	
	# Get the session
	session = fx.activeSession()
	print('[Session] ' + str(session.label) + '\n')
	
	if session is not None:
		# List all properties
		for i in range(len(session.properties.keys())):
			key = session.properties.keys()[i]
			print('\t[Propery] ' + str(key) + ' [Value] "' + str(session.properties[key].value) + '"')


# Create the action
class SessionExplorerAction(Action):
	"""Explore Session Properties."""
	
	def __init__(self):
		Action.__init__(self, 'Developer|Session Explorer')
		
	def available(self):
		assert True
		
	def execute(self):
		run()

addAction(SessionExplorerAction())