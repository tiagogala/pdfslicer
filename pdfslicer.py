#! /usr/bin/python

#########################################################################################
# 											#
#	pdfslicer: A tool for slicing a pdf document page into several smaller pages.	#
#	Copyright (C) 2015  Tiago Filipe Gala da Silva					#
#											#
#	This program is free software; you can redistribute it and/or modify		#
#	it under the terms of the GNU General Public License as published by		#
#	the Free Software Foundation; either version 2 of the License, or		#
#	(at your option) any later version.						#
#											#
#	This program is distributed in the hope that it will be useful,			#
#	but WITHOUT ANY WARRANTY; without even the implied warranty of			#
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the			#
#	GNU General Public License for more details.					#
#											#
#	You should have received a copy of the GNU General Public License along		#
#	with this program; if not, write to the Free Software Foundation, Inc.,		#
#	51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.			#
#											#
#########################################################################################

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

pages_xx = math.ceil((original_size[0]-sm.MINIMUM_X)/paper_x)	#number of pages on xx
pages_yy = math.ceil((original_size[1]-sm.MINIMUM_Y)/paper_y)	#number of pages on yy

# 	original_size-MINIMUM_X means anything that doesn't match this
#	limits won't count for the page numbering!


#actually calculate the page distribution
slicecuts = sm.getslicecuts(pages_xx, pages_yy, paper_x, paper_y)
sm.applyboundaries(slicecuts, original_size[0], original_size[1]) 

#print report
print("Number of pages on the xx axis:", pages_xx)
print("Number of pages on the yy axis:", pages_yy)
print("Total number of pages used:", len(slicecuts))
print("\n")



#run ghostscript commands

resolution = 300 	#dpi

i=0
while len(slicecuts) >= 1:
	cut = slicecuts.pop(0)
	pdfname="_page"+str(i).zfill(3)+".pdf"
	cmd = ["gs -sDEVICE=pdfwrite",
		"-q",
		"-dFirstPage="+str(page),
		"-dLastPage="+str(page),
		"-o",pdfname,
		"-c \"[/TrimBox [0 0 842 1190] /PAGES pdfmark\" "
		"-c \"[/CropBox [", 
		str(cut[0]),	#x1 
		str(cut[2]),	#y1
		str(cut[1]),	#x2
		str(cut[3]),	#y2
		"] /PAGES pdfmark\"",
		"-f",
		input_file]
	

	if dry_run==0:
		os.system(" ".join(cmd))
		#os.system(" ".join(com2))
	i = i+1

print("Sliced", input_file, "into", str(i),papersize.upper(),"sheets." )

#making adjustments
print("Making Adjustments...")
r = os.listdir('.')
for f in r:
	if f.startswith("_page"):
		
		cmd2= ["gs -sDEVICE=pdfwrite -dFIXEDMEDIA -q -r"+str(resolution)+"x"+str(resolution),
			"-g"+str(resolution*paper_y)+"x"+str(resolution*paper_x),
			"-o", "d"+f,
			f]
		os.system(" ".join(cmd2))
		os.remove(f)

#join pdf's into single file
if dry_run==0:
	os.system("gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile="+output+".pdf d_page*.pdf")

#delete old pdf's
r = os.listdir('.')
for f in r:
	if (f.startswith("_page") or f.startswith("d_page")) and dry_run==0:
		os.remove(f)	
