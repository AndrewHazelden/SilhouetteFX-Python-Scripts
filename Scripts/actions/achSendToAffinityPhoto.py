"""
Affinity Photo Script - V1.1 2019-11-26
By Andrew Hazelden <andrew@andrewhazelden.com>
----------------------------------------------

This script will send the currently selected media to Affinity Photo.


# Script Usage # 

Step 1. Select a source media node in the tree.

Step 2. Run the "Actions > Send To > Affinity Photo" menu item.


# Script Installation #

Step 1. Open the Silhouette Script Actions folder using the following terminal command:

open "/Applications/SilhouetteFX/Silhouette v7.5/Silhouette.app/Contents/Resources/scripts/actions/"

Step 2. Install this Python script by copying it to:

/Applications/SilhouetteFX/Silhouette v7.5/Silhouette.app/Contents/Resources/scripts/actions/achSendToAffinityPhoto.py

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
			return getSource(input.pipes[0].source.node)
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
	
	# Build the launching command
	cmd = '/Applications/Affinity Photo.app'
	args = ['open', '-a', cmd, path]
	print('[Launching AffinityPhoto] ' + str(args))

	# Run Open
	# subprocess.call(args)
	subprocess.Popen(args)

# Run the script
def run():
	import fx
	
	# Check the current selection
	node = fx.activeNode()
	
	# Get the session
	session = fx.activeSession()
	
	print('[Affinity Photo]')
	print('\t[Node Name] ' + node.label)
	
	# Process a source node
	if node.type == 'SourceNode':
		# Find the active source node
		source = GetSource(node)
		if source:
			# Get the current node's filepath
			path = source.path(-1)
			
			# Translate #### into the current frame
			padding = int(fx.prefs['render.filename.padding'])
			startFrame = session.startFrame
			currentFrame = int(startFrame + fx.player.frame)
			path = path.replace('####', str(currentFrame).zfill(padding))
			
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
class AffinityPhoto(Action):
	"""View in AffinityPhoto."""
	
	def __init__(self):
		Action.__init__(self, 'Send To|Affinity Photo')
		
	def available(self):
		assert len(selection()) != 0, 'Select a media object.'
		
	def execute(self):
		run()

addAction(AffinityPhoto())
