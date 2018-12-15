"""Encode Movie ProRes Script - V1.0 2018-12-15
By Andrew Hazelden <andrew@andrewhazelden.com>
----------------------------------------------

This script will send the currently selected media to Compressor and encode a MOV file.

# Script Usage # 

Step 1. Select a source media node in the tree.

Step 2. Run the "Actions > Encode Movie > ProRes" menu item.

# Script Installation #

Step 1. Open the Silhouette Script Actions folder using the following terminal command:

open "/Applications/SilhouetteFX/Silhouette v7/Silhouette.app/Contents/Resources/scripts/actions/"

Step 2. Install this Python script by copying it to:

/Applications/SilhouetteFX/Silhouette v7/Silhouette.app/Contents/Resources/scripts/actions/EncodeMovieProRes.py

Step 3. Copy the provided Apple Compressor encoding presets folder named "compressor" to:

/Applications/SilhouetteFX/Silhouette v7/Silhouette.app/Contents/Resources/scripts/compressor

The compressor folder is used as a container to neat and tidily hold your exported ".cmprstng" file.

Step 4. Scroll down in this document and update that filepath and the name of the Apple Compressor exported ".cmprstng" preset file you want to use with the current "achEncodeMovie.py" script.

	# Compressor preset
	settings = '/Applications/SilhouetteFX/Silhouette v7/Silhouette.app/Contents/Resources/scripts/compressor/ProRes.cmprstng'

Step 5. Restart SilhouetteFX to re-load the active scripts, and start creating new art, new possibilities, and making new creative visions come to life!

# Bonus Tip #

Apple Compressor's CLI mode expects your image sequence to be rendered into a new, custom output folder. The files present in that folder, in linear order will be turned into your movie file.

Compressor can work with DWAA encoded EXRs that have RGBA data in them. You will have to use SilhouetteFX and its Render Session mode to bounce out a temporary RGBA channel EXR sequence if you want to encode an MP4 or ProRes movie from it using this script.

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

# Compress a movie from the folder path
def EncodeMovie(path):
	import os
	import subprocess
	
	# Trim the filepath down to the parent folder
	dir = os.path.dirname(path)
	
	# Compressor preset
	settings = '/Applications/SilhouetteFX/Silhouette v7/Silhouette.app/Contents/Resources/scripts/compressor/ProRes.cmprstng'
	
	# Compressor Job name
	batch = 'sfx+'
	
	# Movie Extension
	ext = 'mov'
	
	# Make the output movie filename
	dest = dir + os.sep + 'ProRes_Encode.' + ext
	
	# Build the Compressor launching command
	cmd = '/Applications/Compressor.app/Contents/MacOS/Compressor'
	args = [cmd, '-batchname', batch, '-jobpath', dir, '-settingpath', settings, '-locationpath', dest]
	print('\t[Launching Compressor] ' + str(args))
	
	# Run Compressor
	# subprocess.call(args)
	subprocess.Popen(args)

# Run the script
def run():
	import fx
	
	# Check the current selection
	node = fx.activeNode()
	
	print('[Encode Movie ProRes]')
	print('\t[Node Name] ' + node.label)
	
	# Start the undo operation
	fx.beginUndo('Encode Movie')
	
	# Process a source node
	if node.type == 'SourceNode':
		# Find the active source node
		source = GetSource(node)
		if source:
			# Get the current node's filepath
			path = source.path(-1)
			print('\t[Image] ' + path)
			
			# Generate the movie
			EncodeMovie(path)
		else:
			print('\t[Error] Select a Source or Output Node.')
	elif node.type == 'OutputNode':
		# Find the active OutputNode path
		path = GetOutput(node)
		print('\t[Image] ' + path)
		
		# Generate the movie
		EncodeMovie(path)
	else:
		print('\t[Error] Select a Source or Output Node.')
	
	# Finish the Undo operation
	fx.endUndo()

# Create the action
class EncodeMovieProRes(Action):
	"""Encode a movie in Compressor."""
	
	def __init__(self):
		Action.__init__(self, 'Encode Movie|ProRes')
		
	def available(self):
		assert len(selection()) != 0, 'Select a Source or Output node.'
		
	def execute(self):
		run()

addAction(EncodeMovieProRes())
