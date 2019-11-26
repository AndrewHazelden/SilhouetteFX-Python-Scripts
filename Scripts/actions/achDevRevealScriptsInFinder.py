"""
Reveal Scripts in Finder - V1.1 2019-11-26
By Andrew Hazelden <andrew@andrewhazelden.com>
----------------------------------------------

This script will reveal the sfx scripts folder in a Finder folder view.

# Script Usage # 

Step 1. Select a Source or Output node in the tree.

Step 2. Run the "Actions > Developer > Reveal Scripts in Finder" menu item.


# Script Installation #

Step 1. Open the Silhouette Script Actions folder using the following terminal command:

open "/Applications/SilhouetteFX/Silhouette v7.5/Silhouette.app/Contents/Resources/scripts/actions/"

Step 2. Install this Python script by copying it to:

/Applications/SilhouetteFX/Silhouette v7.5/Silhouette.app/Contents/Resources/scripts/actions/DevRevealScriptsInFinder.py

Step 3. Restart SilhouetteFX to re-load the active scripts.
"""

# Import the modules
from fx import *
from tools.objectIterator import ObjectIterator
import hook

# Run a shell command
def Command():
	import os
	import subprocess
	
	dir = '/Applications/SilhouetteFX/Silhouette v7.5/Silhouette.app/Contents/Resources/scripts'
	
	# Make the output filename
	dest = dir + os.sep
	
	# Build the launching command
	cmd = 'open'
	args = [cmd, dest]
	print('\t[Launching Open] ' + str(args))
	
	# Run Open
	# subprocess.call(args)
	subprocess.Popen(args)

# Run the script
def run():
	import fx
	
	# Check the current selection
	node = fx.activeNode()
	
	print('[Reveal Scripts in Finder]')
	print('\t[Node Name] ' + node.label)
	
	# Reveal Scripts in Finder
	Command()

# Create the action
class RevealScriptsInFinder(Action):
	"""Encode a movie in Compressor."""
	
	def __init__(self):
		Action.__init__(self, 'Developer|Reveal Scripts in Finder')
		
	def available(self):
		assert True
		
	def execute(self):
		run()

addAction(RevealScriptsInFinder())

