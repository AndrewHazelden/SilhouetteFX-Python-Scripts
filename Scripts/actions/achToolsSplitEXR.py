"""
SplitEXR Script - V1.1 2019-11-26
By Andrew Hazelden <andrew@andrewhazelden.com>
----------------------------------------------

This script will split the currently selected source EXR media.


# Script Usage # 

Step 1. Select a source media node in the tree.

Step 2. Run the "Actions > Tools > SplitEXR" menu item.


# Script Installation #

Step 1. Open the Silhouette Script Actions folder using the following terminal command:

open "/Applications/SilhouetteFX/Silhouette v7.5/Silhouette.app/Contents/Resources/scripts/actions/"

Step 2. Install this Python script by copying it to:

/Applications/SilhouetteFX/Silhouette v7.5/Silhouette.app/Contents/Resources/scripts/actions/ToolsSplitEXR.py

Step 3. Restart SilhouetteFX to re-load the active scripts.

"""

# Import the modules
from fx import *
from tools.objectIterator import ObjectIterator

# Run the script
def run():
	print('[Split EXR]')
	
	beginUndo('Create Source Layers')
	project = activeProject()
	
	try:
		source = selection()[0]
		for layer in source.layers:
			if layer != 'default':
				print '\t[Creating Layer] ' + layer
				path = source.property('path').value
				s = Source(path)
				project.addItem(s)
				s.property('layer').value = layer
	except Exception as e:
		print e
	
	endUndo()

# Create the action
class SplitEXR(Action):
	"""SplitEXR."""
	
	def __init__(self):
		Action.__init__(self, 'Tools|SplitEXR')
		
	def available(self):
		assert len(selection()) != 0, 'Select a media object.'
		
	def execute(self):
		run()

addAction(SplitEXR())
