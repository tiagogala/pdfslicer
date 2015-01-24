#! /usr/bin/python

import sys
import os.path
import slicermodules as sm

# RUN THIS:
#	 gs  -sDEVICE=pdfwrite -o marked.pdf -c "[/CropBox [54 54 1314 810] /PAGES pdfmark" -f original.pdf
#

if len(sys.argv) == 1:
	print('''Usage: pdfslicer inputfile.pdf [Options]
	Options:
	-p page		Choose which page to slice
	-s 		Print dimensions of inputfile
	-o output	Output file name
	-O orientation	Choose page orientation (l for landscape, p for portrait)
	-P papersize	Choose output paper size (A6, A5, A4, A3, A2, A1, A0)''')
	sys.exit()
else:
	#set defaults:
	page=1
	orientation='l'
	papersize='a4'
	output="output.pdf"

	#process args
	sys.argv.pop(0)		#first arg is the script name, it's not useful
	input_file=sys.argv.pop(0)	
	#check if file exists
	if not os.path.isfile(input_file):
		sys.exit("Error: Bad input file: "+input_file)

	#processing args:
	while len(sys.argv) >= 1:
		arg = sys.argv.pop(0)
		
		if arg=="-p":	#choose page
			if len(sys.argv) >= 1:
				page = sys.argv.pop(0)
				if not page.isdigit():
					sys.exit("Error: Bad page number: "+page)
					#check if is in range? gs will complain... FIXME
			else:
				sys.exit("Error: No page number specified, -p switch can be ommited if the target is the first page only.")

		if arg=="-s":	#FIXME: if other than page 1, this switch must be placed after -p 
			print("Page size:", sm.getsize(input_file, page))
		
		if arg=="-o":
			if len(sys.argv) >= 1:
				output=sys.argv.pop(0)
			else:
				sys.exit("Error: No output filename specified.")

		if arg=="-O":
			if len(sys.argv) >= 1:
				orientation=sys.argv.pop(0).lower()
				if not (orientation=="l" or orientation=="p"):
					sys.exit("Error: Bad orientation: "+orientation)
			else:
				sys.exit("Error: No orientation specified")

		if arg=="-P":
			if len(sys.argv) >= 1:
				papersize=sys.argv.pop(0).lower()
				if not papersize in ["a0", "a1", "a2", "a3", "a4", "a5", "a6"]:
					sys.exit("Error: Unrecognized paper size: "+papersize)
			else:
				sys.exit("Error: No paper size specified.")

	# DEBUG
#	print("Using the following options:",[input_file, page, output, orientation, papersize])

	

