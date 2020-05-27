#!python3
import os
import subprocess
import re
import sys
import time

def findLayers():
	print('Getting dumpsys for devicestate')
	dumpsys=subprocess.getoutput(["adb","shell","dumpsys","SurfaceFlinger"])
	dump_list=dumpsys.split("\n")
	print('Processing dumpsys for layers info')
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
def wake():
	result = subprocess.getoutput("adb shell dumpsys display | grep mScreenState")
	if(result!=None):
		pattern=re.search(r'^.*mScreenState=(\S+)',result)
		state=pattern.group(1)
	if(state==""):
		print("Could not find screenstate, please retry")
	elif(state=="OFF"):
		print('Display is in OFF state, waking it now')
		os.system("adb wait-for-device shell input keyevent 26")
		os.system("adb wait-for-device shell input keyevent 82")
		os.system("adb wait-for-device shell input keyevent 3")
	elif(state=="ON"):
		print('Display is in ON state')
	elif(state=="DOZE"):
		print('Display is in DOZE state')
		os.system("adb wait-for-device shell input keyevent 26")
		os.system("adb wait-for-device shell input keyevent 82")
		os.system("adb wait-for-device shell input keyevent 3")

wake()
