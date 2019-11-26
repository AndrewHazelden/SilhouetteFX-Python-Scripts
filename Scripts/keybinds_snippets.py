## Usage: Paste this file's contents into the top of the sfx "scripts/keybinds.py" file

import fx

#
# Helper function which returns a function that calls
# a specified method of an object, passing in the argument list.
# Used to replace 'lambda', which is being phased out
#
def callMethod(func, *args, **kwargs):
	def _return_func():
		return func(*args, **kwargs)
	return _return_func


# -----------------------------------------
# ACH MacOS keybinds Start - 2019-11-26
# "g" hotkey runs a node alignment script
# "r" hotkey runs a "Reveal in Finder" script
# "tab" hotkey runs a "Send To > DJV View" script
# -----------------------------------------

import hook

# Return the Source node's master source clip
def GetSource(node):
	if node:
		if node.type == "SourceNode":
			props = node.properties
			primary = props["stream.primary"]
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

def runDJV():
	import fx
	import subprocess
	
	node = fx.activeNode()

	# Find the active source node
	source = GetSource(node)
	if source:
		# Get the current node's filepath
		path = source.path(-1)
		print("[Image] " + path)
	
		# Build the DJV_View launching command
		cmd = "/Applications/DJV.app/Contents/Resources/bin/djv_view.sh"
		args = [cmd, path]
		print("[Launching DJV] " + str(args))
	
		# Run DJV_View
		#subprocess.call(args)
		subprocess.Popen(args)
	else:
		print("[Error] Select a media object.")

fx.bind("tab", runDJV)

# Run a shell command
def OpenCommand(path):
	import os
	import subprocess
	
	# Trim the filepath down to the parent folder
	dir = os.path.dirname(path)
	
	# Make the output movie filename
	dest = dir + os.sep
	
	# Build the launching command
	cmd = 'open'
	args = [cmd, dest]
	print('\t[Launching Open] ' + str(args))
	
	# Run Open
	# subprocess.call(args)
	subprocess.Popen(args)

# Show the Source or Output node in a Finder window
def runRevealInFinder():
	import fx
	
	# Check the current selection
	node = fx.activeNode()
	
	print('[Reveal in Finder]')
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
			OpenCommand(path)
		else:
			print('\t[Error] Select a Source or Output Node.')
	elif node.type == 'OutputNode':
		# Find the active OutputNode path
		path = GetOutput(node)
		print('\t[Image] ' + path)
		
		# Reveal in Finder
		OpenCommand(path)
	else:
		print('\t[Error] Select a Source or Output Node.')

fx.bind("r", runRevealInFinder)

# Align Nodes Window
# 2018-10-27 01.00 PM

def AlignVertical():
	import fx
	
	tool = 'Align Vertical'
	PrintStatus(tool)
	fx.beginUndo(tool)
	
	# Get the Project
	project = fx.activeProject()
	
	# Get the node selection
	sel = fx.selection()
	
	# Padding width for node count
	padding = len(str(len(sel)))
	
	# Use the first selected object as a reference for the Node Y height
	referenceY = 0
	if len(sel) > 1:
		referenceY = sel[0].state.items()[1][1].y
		print('[Reference Y] ' + str(referenceY))
		
		# Scan all of the selected nodes
		i=0
		for node in sel:
			i = i + 1
			# The node.state dict holds {'viewMode': 0, 'graph.pos': Point3D(394.641,22.4925)}
			if node.state is not None:
				# The Point3D(0,0) datatype has .x and .y attributes
				pos = node.state.items()[1][1]
				if pos is not None:
					# Snap all the nodes to the same Y height
					node.setState('graph.pos', fx.Point3D(pos.x,referenceY))
					
					# Read back the results
					posUpdate = node.state.items()[1][1]
					if posUpdate is not None:
						print('[' + str(i).zfill(padding) + '] ' + str(node.label) + ' [Original] [X]' + str(pos.x) + ' [Y] ' + str(pos.y) + ' [Updated] [X]' + str(posUpdate.x) + ' [Y] ' + str(posUpdate.y))
	else:
		print('[Error] Please select 2 or more nodes.')
	
	fx.endUndo()
	
	# SaveProject()
	
	# hide the window
	snapWindow.hide()

def AlignHorizontal():
	import fx
	
	tool = 'Align Horizontal'
	PrintStatus(tool)
	fx.beginUndo(tool)
	
	# Get the Project
	project = fx.activeProject()
	
	# Get the node selection
	sel = fx.selection()
	
	# Padding width for node count
	padding = len(str(len(sel)))
	
	# Use the first selected object as a reference for the Node X position
	referenceX = 0
	if len(sel) > 0:
		referenceX = sel[0].state.items()[1][1].x
		print('[Reference X] ' + str(referenceX))
		
		# Scan all of the selected nodes
		i=0
		for node in sel:
			i = i + 1
			# The node.state dict holds {'viewMode': 0, 'graph.pos': Point3D(394.641,22.4925)}
			if node.state is not None:
				# The Point3D(0,0) datatype has .x and .y attributes
				pos = node.state.items()[1][1]
				if pos is not None:
					# Snap all the nodes to the same X height
					node.setState('graph.pos', fx.Point3D(referenceX, pos.y))
					
					# Read back the results
					posUpdate = node.state.items()[1][1]
					if posUpdate is not None:
						print('[' + str(i).zfill(padding) + '] ' + str(node.label) + ' [Original] [X]' + str(pos.x) + ' [Y] ' + str(pos.y) + ' [Updated] [X]' + str(posUpdate.x) + ' [Y] ' + str(posUpdate.y))
	else:
		print('[Error] Please select 2 or more nodes.')
	
	fx.endUndo()
	
	# SaveProject()
	
	# hide the window
	snapWindow.hide()

def StackHorizontal():
	import fx
	
	tool = 'Stack Horizontal'
	PrintStatus(tool)
	fx.beginUndo(tool)

	# Get the Project
	project = fx.activeProject()
	
	# Get the node selection
	sel = fx.selection()
	
	# Padding width for node count
	padding = len(str(len(sel)))

	# Spacing distance between stacked nodes
	nodeSpacing = 200
	
	# Use the first selected object as a reference for the Node X position
	referenceX = 0
	if len(sel) > 0:
		referenceX = sel[0].state.items()[1][1].x
		print('[Reference X] ' + str(referenceX))
		
		# Scan all of the selected nodes
		i=0
		for node in sel:
			# The node.state dict holds {'viewMode': 0, 'graph.pos': Point3D(394.641,22.4925)}
			if (node.state is not None) and (node != sel[0]):
				i = i + 1
				# The Point3D(0,0) datatype has .x and .y attributes
				pos = node.state.items()[1][1]
				if pos is not None:
					# Stack the nodes side by side
					node.setState('graph.pos', fx.Point3D((referenceX + (i * nodeSpacing)), pos.y))
					
					# Read back the results
					posUpdate = node.state.items()[1][1]
					if posUpdate is not None:
						print('[' + str(i).zfill(padding) + '] ' + str(node.label) + ' [Original] [X]' + str(pos.x) + ' [Y] ' + str(pos.y) + ' [Updated] [X]' + str(posUpdate.x) + ' [Y] ' + str(posUpdate.y))
	else:
		print('[Error] Please select 2 or more nodes.')
	fx.endUndo()
	
	# SaveProject()
	
	# hide the window
	snapWindow.hide()

def StackVertical():
	import fx
	
	tool = 'Stack Vertical'
	PrintStatus(tool)
	fx.beginUndo(tool)
	
	# Get the Project
	project = fx.activeProject()
	
	# Get the node selection
	sel = fx.selection()
	
	# Padding width for node count
	padding = len(str(len(sel)))

	# Spacing distance between stacked nodes
	nodeSpacing = 100
	
	# Use the first selected object as a reference for the Node Y position
	referenceY = 0
	if len(sel) > 0:
		referenceY = sel[0].state.items()[1][1].y
		print('[Reference Y] ' + str(referenceY))
		
		# Scan all of the selected nodes
		i=0
		for node in sel:
			# The node.state dict holds {'viewMode': 0, 'graph.pos': Point3D(394.641,22.4925)}
			if (node.state is not None) and (node != sel[0]):
				i = i + 1
				# The Point3D(0,0) datatype has .x and .y attributes
				pos = node.state.items()[1][1]
				if pos is not None:
					# Stack the nodes side by side
					node.setState('graph.pos', fx.Point3D(pos.x, (referenceY + (i * nodeSpacing))))
					
					# Read back the results
					posUpdate = node.state.items()[1][1]
					if posUpdate is not None:
						print('[' + str(i).zfill(padding) + '] ' + str(node.label) + ' [Original] [X]' + str(pos.x) + ' [Y] ' + str(pos.y) + ' [Updated] [X]' + str(posUpdate.x) + ' [Y] ' + str(posUpdate.y))
	else:
		print('[Error] Please select 2 or more nodes.')
	
	fx.endUndo()
	
	# SaveProject()
	
	# hide the window
	snapWindow.hide()

def DistributeSpacesVertical():
	import fx
	
	tool = 'Distribute Spaces Vertical'
	PrintStatus(tool)
	fx.beginUndo(tool)
	
	fx.beginUndo()
	
	# Get the Project
	project = fx.activeProject()
	
	# Get the node selection
	sel = fx.selection()
	
	# Padding width for node count
	padding = len(str(len(sel)))
	
	# How many does were selected
	nodeCount = len(sel)
	
	# Use the first selected object as a reference for the Node position
	referenceStartY = 0
	referenceEndY = 0
	if nodeCount > 0:
		print('[Selected Nodes] ' + str(nodeCount))
		
		referenceStartY = sel[0].state.items()[1][1].y
		print('[Reference Start Y] ' + str(referenceStartY))
		
		referenceEndY = sel[nodeCount-1].state.items()[1][1].y
		print('[Reference End Y] ' + str(referenceEndY))
		
		# Start/End Node Distance
		nodeDistance = abs(referenceStartY - referenceEndY)
		print('[Node Distance Y] ' + str(nodeDistance))
		
		# Spacing distance between stacked nodes
		nodeSpacing = (nodeDistance) / (nodeCount - 1)
		print('[Node Spacing Y] ' + str(nodeSpacing))
		
		# Scan all of the selected nodes
		i=0
		for node in sel:
			# The node.state dict holds {'viewMode': 0, 'graph.pos': Point3D(394.641,22.4925)}
			if (node.state is not None) and (node != sel[0]) and (node != sel[nodeCount-1]):
			# if (node.state is not None):
				i = i + 1
				# The Point3D(0,0) datatype has .x and .y attributes
				pos = node.state.items()[1][1]
				if pos is not None:
					# Stack the nodes side by side
					node.setState('graph.pos', fx.Point3D(pos.x, (referenceStartY + (i * nodeSpacing))))
					
					# Read back the results
					posUpdate = node.state.items()[1][1]
					if posUpdate is not None:
						print('[' + str(i).zfill(padding) + '] ' + str(node.label) + ' [Original] [X]' + str(pos.x) + ' [Y] ' + str(pos.y) + ' [Updated] [X]' + str(posUpdate.x) + ' [Y] ' + str(posUpdate.y))
	else:
		print('[Error] Please select 2 or more nodes.')
	
	fx.endUndo()
	
	# SaveProject()
	
	# hide the window
	snapWindow.hide()
	
def DistributeSpacesHorizontal():
	import fx
	
	tool = 'Distribute Spaces Horizontal'
	PrintStatus(tool)
	fx.beginUndo(tool)
	
	# Get the Project
	project = fx.activeProject()
	
	# Get the node selection
	sel = fx.selection()
	
	# Padding width for node count
	padding = len(str(len(sel)))
	
	# How many does were selected
	nodeCount = len(sel)
	
	# Use the first selected object as a reference for the Node position
	referenceStartX = 0
	referenceEndX = 0
	if nodeCount > 0:
		print('[Selected Nodes] ' + str(nodeCount))
		
		referenceStartX = sel[0].state.items()[1][1].x
		print('[Reference Start X] ' + str(referenceStartX))
		
		referenceEndX = sel[nodeCount-1].state.items()[1][1].x
		print('[Reference End X] ' + str(referenceEndX))
		
		# Start/End Node Distance
		nodeDistance = abs(referenceStartX - referenceEndX)
		print('[Node Distance X] ' + str(nodeDistance))
		
		# Spacing distance between stacked nodes
		nodeSpacing = (nodeDistance) / (nodeCount - 1)
		print('[Node Spacing X] ' + str(nodeSpacing))
		
		# Scan all of the selected nodes
		i=0
		for node in sel:
			# The node.state dict holds {'viewMode': 0, 'graph.pos': Point3D(394.641,22.4925)}
			if (node.state is not None) and (node != sel[0]) and (node != sel[nodeCount-1]):
			# if (node.state is not None):
				i = i + 1
				# The Point3D(0,0) datatype has .x and .y attributes
				pos = node.state.items()[1][1]
				if pos is not None:
					# Stack the nodes side by side
					node.setState('graph.pos', fx.Point3D((referenceStartX + (i * nodeSpacing)), pos.y))
					
					# Read back the results
					posUpdate = node.state.items()[1][1]
					if posUpdate is not None:
						print('[' + str(i).zfill(padding) + '] ' + str(node.label) + ' [Original] [X]' + str(pos.x) + ' [Y] ' + str(pos.y) + ' [Updated] [X]' + str(posUpdate.x) + ' [Y] ' + str(posUpdate.y))
	else:
		print('[Error] Please select 2 or more nodes.')
		
	fx.endUndo()
	
	# SaveProject()
	
	# hide the window
	snapWindow.hide()

def SnapToGrid():
	import fx
	
	tool = 'Snap to Grid'
	PrintStatus(tool)
	fx.beginUndo(tool)
	
	# Get the Project
	project = fx.activeProject()
	
	# Get the node selection
	sel = fx.selection()
	
	# Padding width for node count
	padding = len(str(len(sel)))
	
	i=0
	for node in sel:
		i = i + 1
		# The node.state dict holds {'viewMode': 0, 'graph.pos': Point3D(394.641,22.4925)}
		if node.state is not None:
			# The Point3D(0,0) datatype has .x and .y attributes
			pos = node.state.items()[1][1]
			if pos is not None:
				# Snap the nodes to a 10 unit grid
				#snapX = round(pos.x, -1)
				#snapY = round(pos.y, -1)
				
				# Snap to 50 grid units
				snapX = round(float(pos.x) * 2, -2) * 0.5
				snapY = round(float(pos.y) * 2, -2) * 0.5
				
				# Snap to 100 grid units on X and 50 gird units on Y
				snapX = round(pos.x, -2)
				snapY = round(float(pos.y) * 2, -2) * 0.5
				
				# Snap the nodes to a 100 unit grid
				#snapX = round(pos.x, -2)
				#snapY = round(pos.y, -2)
				
				# Update the grid snapped node position
				node.setState('graph.pos', fx.Point3D(snapX,snapY))
				
				posUpdate = node.state.items()[1][1]
				if posUpdate is not None:
					print('[' + str(i).zfill(padding) + '] ' + str(node.label) + ' [Original] [X]' + str(pos.x) + ' [Y] ' + str(pos.y) + ' [Updated] [X]' + str(posUpdate.x) + ' [Y] ' + str(posUpdate.y))
	
	fx.endUndo()
	
	# SaveProject()
	
	# hide the window
	snapWindow.hide()

def AlignByCSV():
	import fx
	import csv
	
	path = '/Applications/SilhouetteFX/Silhouette v7.5/Silhouette.app/Contents/Resources/scripts/node_shape.csv'
	
	tool = 'Align By CSV'
	PrintStatus(tool)
	fx.beginUndo(tool)
	
	# Get the Project
	project = fx.activeProject()
	
	# Get the node selection
	sel = fx.selection()
	
	# Padding width for node count
	padding = 4
	
	# How many nodes are selected
	count = len(sel)
	
	# Prepare CSV reading
	with open(path, 'rb') as fp:
		reader = csv.reader(fp, delimiter=',')
		
		i=0
		# Scan all of the selected nodes
		for row in reader:
			# Move onto the next node
			# The node.state dict holds {'viewMode': 0, 'graph.pos': Point3D(394.641,22.4925)}
			if i < count:
				node = sel[i]
				if (node.state is not None):
					# The Point3D(0,0) datatype has .x and .y attributes
					node.setState('graph.pos', fx.Point3D(float(row[0]), float(row[1])))
					
					#posUpdate = node.state.items()[1][1]
					#if posUpdate is not None:
						# Read back the results
						# print('{0},{1:.03f},{2:.03f}'.format(str(i).zfill(padding), posUpdate.x, posUpdate.y))
			i = i + 1
		
	fx.endUndo()
	
	# SaveProject()
	
	# hide the window
	snapWindow.hide()

# def SaveByCSV(path):
def SaveByCSV():
	import fx
	import csv
	
	path = '/Applications/SilhouetteFX/Silhouette v7.5/Silhouette.app/Contents/Resources/scripts/node_shape.csv'
	
	# Prepare CSV writing
	with open(path, 'wb') as fp:
		writer = csv.writer(fp, delimiter=',')
		# writer.writerow(['X', 'Y'])
		
		tool = 'Save CSV'
		PrintStatus(tool)
		fx.beginUndo(tool)
		
		# Get the Project
		project = fx.activeProject()
		
		# Get the node selection
		sel = fx.selection()
		
		# Padding width for node count
		padding = len(str(len(sel)))
		
		if len(sel) > 1:
			# Scan all of the selected nodes
			for node in sel:
				# The node.state dict holds {'viewMode': 0, 'graph.pos': Point3D(394.641,22.4925)}
				if node.state is not None:
					# The Point3D(0,0) datatype has .x and .y attributes
					pos = node.state.items()[1][1]
					if pos is not None:
						# Read back the results
						# print('{0:.03f},{1:.03f}'.format(pos.x, pos.y))
						writer.writerow([pos.x, pos.y])
		else:
			print('[Error] Please select 2 or more nodes.')
		
		fx.endUndo()
		
		# Close the CSV file pointer
		# fp.close()

# Print a toolbar button clicked message
def PrintStatus(msg):
	fx.status(msg)
	
	print('\n---------------------------------------------')
	print('[' + msg + ']')
	print('---------------------------------------------\n')
	
def SaveProject():
	import fx
	
	# Get the Project
	project = fx.activeProject()
	
	# Save the project
	project.save()
	
	# Display the results
	# PrintStatus('\n[Saved Project] To see the updated node positions use the "File > Recent Projects >" menu to re-open the current project. Or press the "Command+Option+Shift+P" hotkeys.')

# Close the align nodes window
def CloseSnapDialog():
	snapWindow.hide()

# Create the GUI window
from PySide2 import QtCore, QtWidgets
from PySide2.QtWidgets import QApplication, QPushButton, QLabel
from PySide2.QtGui import QIcon

# Icon and window size
buttonWidth = 32
buttonheight = 32
windowWidth = buttonWidth * 10
windowHeight = buttonheight

# Create the window
snapWindow = QtWidgets.QWidget()
snapWindow.resize(windowWidth, windowHeight)
snapWindow.move(375, 600)
snapWindow.setWindowTitle('Align Nodes')
snapWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)

def SnapDialog():
	# print('[Window] ' + 'Align Nodes')
	
	buttonLabels = ['Align Vertical', 'Align Horizontal', 'Stack Horizontal', 'Stack Vertical', 'Distribute Spaces Horizontal', 'Distribute Spaces Vertical', 'CSV', 'Snap to Grid']
	
	iconFolder = '/Applications/SilhouetteFX/Silhouette v7.5/Silhouette.app/Contents/Resources/scripts/icons/'
	
	# Create the buttons
	button = QPushButton(snapWindow)
	# button.setText('Close Window')
	button.setGeometry(QtCore.QRect(0 * buttonWidth, 0, buttonWidth, buttonheight))
	button.setIcon(QIcon(iconFolder + 'close.png'))
	button.clicked.connect(CloseSnapDialog)
	
	button = QPushButton(snapWindow)
	# button.setText('Align Vertical')
	button.setGeometry(QtCore.QRect(1 * buttonWidth, 0, buttonWidth, buttonheight))
	button.setIcon(QIcon(iconFolder + 'align_vertical.png'))
	button.clicked.connect(AlignVertical)
	
	button = QPushButton(snapWindow)
	# button.setText('Align Horizontal')
	button.setGeometry(QtCore.QRect(2 * buttonWidth, 0, buttonWidth, buttonheight))
	button.setIcon(QIcon(iconFolder + 'align_horizontal.png'))
	button.clicked.connect(AlignHorizontal)
	
	button = QPushButton(snapWindow)
	# button.setText('Stack Horizontal')
	button.setGeometry(QtCore.QRect(3 * buttonWidth, 0, buttonWidth, buttonheight))
	button.setIcon(QIcon(iconFolder + 'stack_horizontal.png'))
	button.clicked.connect(StackHorizontal)
	
	button = QPushButton(snapWindow)
	# button.setText('Stack Vertical')
	button.setGeometry(QtCore.QRect(4 * buttonWidth, 0, buttonWidth, buttonheight))
	button.setIcon(QIcon(iconFolder + 'stack_vertical.png'))
	button.clicked.connect(StackVertical)
	
	button = QPushButton(snapWindow)
	# button.setText('Distribute Spaces Horizontal')
	button.setGeometry(QtCore.QRect(5 * buttonWidth, 0, buttonWidth, buttonheight))
	button.setIcon(QIcon(iconFolder + 'distribute_horizontal.png'))
	button.clicked.connect(DistributeSpacesHorizontal)
	
	button = QPushButton(snapWindow)
	# button.setText('Distribute Spaces Vertical')
	button.setGeometry(QtCore.QRect(6 * buttonWidth, 0, buttonWidth, buttonheight))
	button.setIcon(QIcon(iconFolder + 'distribute_vertical.png'))
	button.clicked.connect(DistributeSpacesVertical)
	
	button = QPushButton(snapWindow)
	# button.setText('Distribute Spaces Vertical')
	button.setGeometry(QtCore.QRect(7 * buttonWidth, 0, buttonWidth, buttonheight))
	button.setIcon(QIcon(iconFolder + 'align_csv.png'))
	button.clicked.connect(AlignByCSV)
	
	button = QPushButton(snapWindow)
	# button.setText('Distribute Spaces Vertical')
	button.setGeometry(QtCore.QRect(8 * buttonWidth, 0, buttonWidth, buttonheight))
	button.setIcon(QIcon(iconFolder + 'save_csv.png'))
	button.clicked.connect(SaveByCSV)
	
	button = QPushButton(snapWindow)
	# button.setText('Snap to Grid')
	button.setGeometry(QtCore.QRect(9 * buttonWidth, 0, buttonWidth, buttonheight))
	button.setIcon(QIcon(iconFolder + 'grid.png'))
	button.clicked.connect(SnapToGrid)
	
	# Display the new window
	snapWindow.show()

fx.bind("g", SnapDialog)

# -----------------------------------------
# ACH keybinds End - 2019-11-26
# -----------------------------------------
