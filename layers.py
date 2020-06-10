#!python3
import os
import sys
import time
from datetime import datetime
import subprocess
import re
def find_layers():
	dump_list=subprocess.getoutput('adb shell dumpsys SurfaceFlinger').split("\n")
	for line_no in range(len(dump_list)):
		if (dump_list[line_no].find("HWC layers:"))>-1:
			first_line=line_no
		if "h/w composer state:" in dump_list[line_no]:
			last_line=line_no
	display_layers_list=dump_list[first_line+1:last_line]
	for line in display_layers_list:
		print(line)
	list = []
	for line in display_layers_list:
		pattern = re.search(r'(.*)\#(.*)',line)
		if(pattern!=None):
			list.append(pattern.group(1))
	return(list)
while 1:
	print(find_layers())
	a=input("Press Enter to continue or Q to exit:")
	if(a.lower()=="q"):
		exit()
