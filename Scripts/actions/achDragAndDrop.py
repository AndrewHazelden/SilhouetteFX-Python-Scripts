"""
Drag and Drop Images + Scripts - V1.0 2018-12-15
By Andrew Hazelden <andrew@andrewhazelden.com>
----------------------------------------------

This script makes it easy to import multiple source images by dropping them into the Trees view. If the EXR image has multi-part or multi-channel elements they will be split into separate sources automatically.

If a Python script is dropped into the Trees view it will be run automatically.


## Script Install ##

Step 1. Copy this Python script into your sfx+ "scripts/actions" folder.

Step 2. Restart sfx+.

Step 3. Drag an image from your desktop into the sfx+ window. It will be loaded into the project's Sources view.


## Drop Hooks Docs ##

http://support.silhouettefx.com/mw/index.php?title=Scripting_Guide#Drop_Hooks

## Todo ##

"""

import fx

# Import Images
def SourcesImport(url):
	import os
	import fx
	from tools.sequenceBuilder import SequenceBuilder
	
	# Grab the current project
	project = fx.activeProject()
	
	# Catch an error when loading media
	try:
		# Create an image sequence from the url
		builder = SequenceBuilder(url)
		
		# Load the media into the project
		src = fx.Source(builder.path)
		
		# Display the results
		statusMsg = '[Import Sources] "' + str(builder.path) + '"'
		fx.status(statusMsg)
		print(statusMsg)
		
		# Layer Names
		print('\t[Layers] ' + str(src.layers))
		
		# Add the images
		if src.layers is not None:
			# Split the EXR multi-part and multi-channel layers apart
			for layer in src.layers:
				print '\t\t[Creating Layer] ' + layer
				
				s = fx.Source(builder.path)
				project.addItem(s)
				
				# Rename the split EXR layer
				# s.label = str(layer)
				s.label = str(s.label) + '_' + str(layer)
				
				# Change the source layer
				if layer != 'default':
					s.property('layer').value = layer
		else:
			# Add the other image types
			project.addItem(src)
	except Exception as e:
		print e

# Run Python Scripts
def RunScript(url):
	import fx
	
	# Display the results
	statusMsg = '[Run Script] "' + str(url) + '"'
	fx.status(statusMsg)
	print(statusMsg)
	
	# Load the Python file from disk
	script = open(url).read()
	
	# Display the script contents
	#print('\t[Code]')
	#print(script)
	
	# Run the script
	try:
		exec(script)
		print('[Done]')
	except:
		print('[Script Error]')

def DragAndDropHook(type, data, coords):
	import os
	import urllib
	import fx
	from tools.sequenceBuilder import SequenceBuilder
	
	# Trim off the trailing newline on the filepaths
	data = data.replace('\r', '')
	
	# Remove the "file://" prefix on filepaths
	data = data.replace('file:///', '/')
	
	# Convert URL encoded characters
	data = urllib.url2pathname(data)
	
	# Process multiple drag and dropped files
	for url in data.split('\n'):
		# Grab the filetype extension
		ext = str(os.path.splitext(url)[-1].lower())
		# print('[File Extension] "' + str(ext) + '"')
		
		# Check the filetypes
		if ext.endswith(('.cin', '.dpx', '.iff', '.jpg', '.jpeg', '.exr', '.sxr', '.png', '.sgi', '.rgb', '.tif', '.tiff', '.tga', '.tpic')):
			# Verify this is an image
			
			# Start the undo point
			fx.beginUndo('Import "' + str(url) + '"')
			
			# Import imagery into the project
			SourcesImport(url)
			
			# Finish Undo
			fx.endUndo()
			
			print('\n')
		elif ext.endswith(('.py', '.py2', '.py3')):
			# Verify this is Python script
			
			# Start the undo point
			fx.beginUndo('Run Script "' + str(url) + '"')
			
			# Import and execute the Python scripts
			RunScript(url)
			
			# Finish Undo
			fx.endUndo()
			
			print('\n')


# Monitor files dragged into the sfx+ window
fx.trees.registerDropHook('text/uri-list', DragAndDropHook)
