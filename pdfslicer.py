#! /usr/bin/python

import sys
import os.path
import slicermodules as sm
import math
import glob

# RUN THIS:
#	 gs  -sDEVICE=pdfwrite -o marked.pdf -c "[/CropBox [54 54 1314 810] /PAGES pdfmark" -f original.pdf
#

if len(sys.argv) == 1:
	print('''Usage: pdfslicer inputfile.pdf [Options]
	Options:
	-p page		Choose which page to slice
	-s 		Print dimensions of inputfile
	-d		Dry-run (don't make changes)
	-o output	Output file name (without extension)
	-O orientation	Choose page orientation (l for landscape, p for portrait)
	-P papersize	Choose output paper size (A6, A5, A4, A3, A2, A1, A0)''')

	sys.exit()
else:
	#set defaults:
	page=1
	orientation='l'
	papersize='a4'
	output="output"
	original_size=(0,0)
	dry_run=0

	#process args
	sys.argv.pop(0)		#first arg is the script name, it's not useful
	input_file=sys.argv.pop(0)	
	#check if file exists
	if not os.path.isfile(input_file):
		sys.exit("Error: Bad input file: "+input_file)
	# get page size
	original_size = sm.getsize(input_file, page)

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
			print("Width:", original_size[0], "\tHeight:", original_size[1] )
			sys.exit(0)
		
		if arg=="-d":
			dry_run=1

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



# PRINT REPORT
print("Width:", original_size[0], "\tHeight:", original_size[1] )
print("Target output size:", papersize.upper(), "\tOrientation:", orientation.upper())

# CONVERT ORIENTATION TO A MORE CONVENIENT FORMAT
if orientation=='p':
	orientation=0
if orientation=='l':
	orientation=1

#calculate page distribution
paper_x = sm.aformat_size[papersize][(orientation+0)&0x01]	#current sheet size width
paper_y = sm.aformat_size[papersize][(orientation+1)&0x01]	#current sheet size height

pages_xx = math.ceil(original_size[0]/paper_x)	#number of pages on xx
pages_yy = math.ceil(original_size[1]/paper_y)	#number of pages on yy

#actually calculate the page distribution
slicecuts = sm.getslicecuts(pages_xx, pages_yy, paper_x, paper_y)
sm.applyboundaries(slicecuts, original_size[0], original_size[1]) 
#actually calculate the page distribution
slicecuts = sm.getslicecuts(pages_xx, pages_yy, paper_x, paper_y)
pages_xx, pages_yy = sm.applyboundaries(slicecuts, original_size[0], original_size[1]) 

#print report
print("Number of pages on the xx axis:", pages_xx)
print("Number of pages on the yy axis:", pages_yy)
print("Total number of pages used:", len(slicecuts))
print("\n")



#run ghostscript commands
i=0
while len(slicecuts) >= 1:
	cut = slicecuts.pop(0)
	com = ["gs -sDEVICE=pdfwrite",
		"-q",
		"-o","_page"+str(i).zfill(3)+".pdf",
		"-c \"[/CropBox [", 
		str(cut[0]),	#x1 
		str(cut[2]),	#y1
		str(cut[1]),	#x2
		str(cut[3]),	#y2
		"] /PAGES pdfmark\"",
		"-f",
		input_file]
	
	if dry_run==0:
		os.system(" ".join(com))

	i = i+1

print("Sliced", input_file, "into", str(i),papersize.upper(),"sheets." )

#join pdf's into single file
if dry_run==0:
	os.system("gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile="+output+".pdf _page*.pdf")

#delete old pdf's
r = os.listdir('.')
for f in r:
	if f.startswith("_page"):
		print(f)
