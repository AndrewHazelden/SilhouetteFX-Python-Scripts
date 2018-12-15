"""
DJV Script - V1.0 2018-12-15
By Andrew Hazelden <andrew@andrewhazelden.com>
----------------------------------------------

This script will send the currently selected media to DJV.


# Script Usage # 

Step 1. Select a source media node in the tree.

Step 2. Run the "Actions > Send To > DJV View" menu item.


# Script Installation #

Step 1. Open the Silhouette Script Actions folder using the following terminal command:

open "/Applications/SilhouetteFX/Silhouette v7/Silhouette.app/Contents/Resources/scripts/actions/"

Step 2. Install this Python script by copying it to:

/Applications/SilhouetteFX/Silhouette v7/Silhouette.app/Contents/Resources/scripts/actions/achSendToDJV.py

Step 3. Restart SilhouetteFX to re-load the active scripts.

"""

# Import the modules
from fx import *
from tools.objectIterator import ObjectIterator
import hook

# Return the Source node's master source clip
def GetSource(node):
	if node:
		if node.type == 'SourceNode':
			props = node.properties
			primary = props['stream.primary']
			return primary.getValue()
		
		input = node.getInput()
		if input.pipes:
			return GetSource(input.pipes[0].source.node)
	return None

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

# Run a shell command
def Command(path):
	import os
	import subprocess
	
	# Build the DJV_View launching command
	# cmd = '/Applications/djv-1.2.1-OSX-x64.app/Contents/Resources/bin/djv_view.sh'
	
	cmd = '/Applications/djv.app/Contents/Resources/bin/djv_view.sh'
	args = [cmd, path]
	print('\t[Launching DJV] ' + str(args))
	
	# Run Open
	# subprocess.call(args)
	subprocess.Popen(args)

# Run the script
def run():
	import fx
	
	# Check the current selection
	node = fx.activeNode()
	
	print('[DJV]')
	print('\t[Node Name] ' + node.label)
	
	# Process a source node
	if node.type == 'SourceNode':
		# Find the active source node
		source = GetSource(node)
		if source:
			# Get the current node's filepath
			path = source.path(-1)
			print('\t[Image] ' + path)
			
			# Reveal in Finder
			Command(path)
		else:
			print('\t[Error] Select a Source or Output Node.')
	elif node.type == 'OutputNode':
		# Find the active OutputNode path
		path = GetOutput(node)
		print('\t[Image] ' + path)
		
		# Reveal in Finder
		Command(path)
	else:
		print('\t[Error] Select a Source or Output Node.')


# Create the action
class DJV(Action):
	"""View in DJV."""
	
	def __init__(self):
		Action.__init__(self, 'Send To|DJV View')
		
	def available(self):
		assert len(selection()) != 0, 'Select a Source or Output Node.'
		
	def execute(self):
		run()

addAction(DJV())
