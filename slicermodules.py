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


version='1'

import sys, subprocess, os, math

MINIMUM_X = 36 	#half inch
MINIMUM_Y = 36

def getsize(input_file, page):
	"Read page size info by calling pdfinfo"
	
	info = subprocess.check_output(['pdfinfo', '-f', str(page), '-l', str(page), input_file])
	info_list = info.split()

	for i in range(0, len(info_list)-1):
		if (info_list[i].decode("utf-8") == "Page") and (info_list[i+2].decode("utf-8") == "size:"):
			return(math.floor(float(info_list[i+3].decode("utf-8"))), math.floor(float(info_list[i+5].decode("utf-8"))))

	return "Page not found."


#define available paper sizes	
aformat_size = {'a0':(2384,3371),
		'a1':(1685,2384),
		'a2':(1190,1684),
		'a3':( 842,1190),
		'a4':( 595, 842),
		'a5':( 420, 595),
		'a6':( 298, 420),
		'a7':( 210, 298),
		'a8':( 148, 210)}


def getslicecuts(pages_xx, pages_yy, paper_x,paper_y, verbose=0):
	"Returns a list of the cropping box for each page"

	#pages_xx: number of pages in xx axis
	#pages_yy: number of pages in yy axis
	#paper_x: paper size in x direction
	#paper_y: paper size in y direction

	slicecuts = []
	
	i=0
	for yy in range(pages_yy-1, 0-1, -1):				#changed order for a more natural approach on the final file
		for xx in range(0, pages_xx):	
			slicecuts.append([xx*paper_x, (xx+1)*paper_x, yy*paper_y, (yy+1)*paper_y])
			if verbose !=0:
				print("\tPage "+str(i)+":\t","x1:", slicecuts[i][0],"x2",slicecuts[i][1] , "y1",slicecuts[i][2] , "y2", slicecuts[i][3])	
			i = i+1
	return slicecuts

def applyboundaries(cuts, max_x, max_y):
	"Limits the output file boundaries to match the input file"

	rm_list = []
	#apply top boundaries
	for a in range(0, len(cuts)):
#		if cuts[a][0] > max_x:
#			cuts[a][0] = max_x
#		if cuts[a][1] > max_x:
#			cuts[a][1] = max_x
#
#		if cuts[a][2] > max_y:
#			cuts[a][2] = max_y
#		if cuts[a][3] > max_y:
#			cuts[a][3] = max_y

		#apply minimum size rules
		if cuts[a][1]-cuts[a][0] <= MINIMUM_X:
			rm_list.append(cuts[a])

		if cuts[a][3]-cuts[a][2] <= MINIMUM_Y:
			rm_list.append(cuts[a])

	#actually remove items
	for item in rm_list:
		cuts.remove(item)
