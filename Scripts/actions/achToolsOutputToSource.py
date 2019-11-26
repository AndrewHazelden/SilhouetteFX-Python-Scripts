"""
Output to Source - V1.1 2019-11-26
By Andrew Hazelden <andrew@andrewhazelden.com>
----------------------------------------------

This script will take the selected Output node and create a new source from it.


# Script Usage # 

Step 1. Select an Output node in the tree.

Step 2. Run the "Actions > Tools > Output to Source" menu item.


# Script Installation #

Step 1. Open the Silhouette Script Actions folder using the following terminal command:

open "/Applications/SilhouetteFX/Silhouette v7.5/Silhouette.app/Contents/Resources/scripts/actions/"

Step 2. Install this Python script by copying it to:

/Applications/SilhouetteFX/Silhouette v7.5/Silhouette.app/Contents/Resources/scripts/actions/ToolsOutputToSource.py

Step 3. Restart SilhouetteFX to re-load the active scripts.

"""

# Import the modules
from fx import *
from tools.objectIterator import ObjectIterator
import hook

# Return the Output node's filepath
def GetOutput(node):
	import fx
	
	# Get the session
	session = fx.activeSession()
	
	if node:
		if node.type == 'OutputNode':
			# Build the current frame
			padding = int(fx.prefs['render.filename.padding'])
			startFrame = session.startFrame
			currentFrame = int(startFrame + fx.player.frame)
			
			# Build the file format
			formatList = ('.cin', '.dpx', '.iff', '.jpg', '.exr', '.png', '.sgi', '.tif', '.tga')
			format = node.properties['format'].value
			formatFancy = formatList[format]
			
			# Build the filename
			path = node.properties['path'].value + '.' + str(currentFrame).zfill(padding) + formatFancy
			return path
	
	return None


# Run the script
def run():
	import fx
	from tools.sequenceBuilder import SequenceBuilder
	
	# Grab the current project
	project = fx.activeProject()
	
	# Check the current selection
	node = fx.activeNode()
	
	print('[Output To Source]')
	print('\t[Node Name] ' + node.label)
	
	# Process a source node
	if node.type == 'OutputNode':
		# Find the active OutputNode path
		path = GetOutput(node)
		print('\t[Image] ' + path)
		
		# Create an image sequence from the url
		builder = SequenceBuilder(path)
		
		# Load the media into the project
		src = fx.Source(builder.path)
		
		# Add the other image types
		project.addItem(src)
	else:
		print('\t[Error] Select a Source or Output Node.')


# Create the action
class OutputToSource(Action):
	"""View in DJV."""
	
	def __init__(self):
		Action.__init__(self, 'Tools|Output To Source')
		
	def available(self):
		assert len(selection()) != 0, 'Select an Output Node.'
		
	def execute(self):
		run()

addAction(OutputToSource())
