#! /usr/bin/python
version='1'

import sys, subprocess, os


def getsize(input_file, page):
	"Read page size info by calling pdfinfo"
	
	info = subprocess.check_output(['pdfinfo', '-f', str(page), '-l', str(page), input_file])
	info_list = info.split()

	for i in range(0, len(info_list)-1):
		if (info_list[i].decode("utf-8") == "Page") and (info_list[i+2].decode("utf-8") == "size:"):
			return(float(info_list[i+3].decode("utf-8")), float(info_list[i+5].decode("utf-8")))

	return "Page not found."


#define available paper sizes	
aformat_size = {'a0':(2384,3371),
		'a1':(1685,2384),
		'a2':(1190,1684),
		'a3':( 842,1190),
		'a4':( 595, 842),
		'a5':( 420, 595)}


def getslicecuts(pages_xx, pages_yy, paper_x,paper_y, verbose=0):
	"Returns a list of the cropping box for each page"

	#pages_xx: number of pages in xx axis
	#pages_yy: number of pages in yy axis
	#paper_x: paper size in x direction
	#paper_y: paper size in y direction

	slicecuts = []
	
	i=0
	for xx in range(0, pages_xx):
		for yy in range(0, pages_yy):	
			slicecuts.append([xx*paper_x, (xx+1)*paper_x, yy*paper_y, (yy+1)*paper_y])
			if verbose !=0:
				print("\tPage "+str(i)+":\t","x1:", slicecuts[i][0],"x2",slicecuts[i][1] , "y1",slicecuts[i][2] , "y2", slicecuts[i][3])	
			i = i+1
	return slicecuts

#def applyboundaries(max_x, max_y, cuts):
#	"Limits "
