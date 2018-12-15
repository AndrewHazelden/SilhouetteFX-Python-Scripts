"""
Project Explorer V1 - 2018-12-15
By Andrew Hazelden <andrew@andrewhazelden.com>
----------------------------------------------
"""

from fx import *

def run():
	import fx

	print('\n\n---------------------------------------------------------------------------------')
	print('Project Explorer')
	print('---------------------------------------------------------------------------------\n')

	# Get the Project
	project = fx.activeProject()
	print('[Project]')
	print('\n\t[Project Path] ' + str(project.label))
	print('\n\t[Project Version] ' + str(project.version))

	print('\n\t[Project Sources]')
	for s in project.sources:
		print('\t\t[Sources] ' + str(s.label))
	
	print('\n\t[Project Sessions]')
	for s in project.sessions:
		print('\t\t[Sesssion] ' + str(s.label))

	# List all properties
	print('\n\t[Project Properties]')
	for i in range(len(project.properties.keys())):
		key = project.properties.keys()[i]
		print('\t\t[Property] ' + str(key) + ' [Value] "' + str(project.properties[key].value) + '"')


# Create the action
class ProjectExplorerAction(Action):
	"""Explore Project Properties."""
	
	def __init__(self):
		Action.__init__(self, 'Developer|Project Explorer')
		
	def available(self):
		assert True
		
	def execute(self):
		run()

addAction(ProjectExplorerAction())