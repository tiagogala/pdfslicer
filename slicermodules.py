#! /usr/bin/python
version='1'

import sys, subprocess, os


def getsize(input_file, page):
	info = subprocess.check_output(['pdfinfo', '-f', str(page), '-l', str(page), input_file])
	info_list = info.split()

	for i in range(0, len(info_list)-1):
	#	print(str(info_list[i].decode("utf-8")))
		if (info_list[i].decode("utf-8") == "Page") and (info_list[i+2].decode("utf-8") == "size:"):
			return(float(info_list[i+3].decode("utf-8")), float(info_list[i+5].decode("utf-8")))

	return "Page not found."
