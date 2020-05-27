#!python3
import os
import subprocess
import re
import sys
import time
def wake():
	result = subprocess.getoutput("adb shell dumpsys display | grep mScreenState")
	if(result!=None):
		pattern=re.search(r'^.*mScreenState=(\S+)',result)
		state=pattern.group(1)
	if(state==""):
		print("Could not find screenstate, please retry")
	elif(state=="OFF"):
		os.system("adb wait-for-device shell input keyevent 26")
		os.system("adb wait-for-device shell input keyevent 82")
		os.system("adb wait-for-device shell input keyevent 3")
	elif(state=="ON" or "DOZE"):
		os.system("adb wait-for-device shell input keyevent 82")
		os.system("adb wait-for-device shell input keyevent 82")
		os.system("adb wait-for-device shell input keyevent 3")
def findLayers():
	dumpsys=(subprocess.getoutput(["adb","shell","dumpsys","SurfaceFlinger"]))
	dump_list=dumpsys.split("\n")
	for line_no in range(len(dump_list)):
		if (dump_list[line_no].find("HWC layers:"))>-1:
			first_line=line_no
		if "h/w composer state:" in dump_list[line_no]:
			last_line=line_no
	display_layers_list=dump_list[first_line+1:last_line]

	list = []
	for line in display_layers_list:
		pattern = re.search(r'(.*)\#(.*)',line)
		if(pattern!=None):
			list.append(pattern.group(1).strip())
	return(list)

def init():
	print('Waiting for device')
	os.system('adb wait-for-device')
	print('Rooting device')
	os.system('adb root')
	print('Moving to home screen')

	while True:
		try:
			subprocess.getoutput('adb wait-for-device shell input keyevent 82')

			layers = findLayers()
			if(len(layers)>1):
				wake()
				print('Setting screen timeout to 20 hours')
				os.system("adb wait-for-device shell settings put system screen_off_timeout 72000000")
				time.sleep(0.5)
				break
		except:
			pass

init()
