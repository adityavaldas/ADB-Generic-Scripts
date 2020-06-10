#!python3
import subprocess
import re
import sys
import time

def findLayers():
	while True:
		try:
			dump_list=subprocess.getoutput('adb shell dumpsys SurfaceFlinger').split("\n")
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
					list.append(pattern.group(1))
			return(list)
		except:
			pass

def init():
	print('Waiting for device')
	subprocess.getoutput('adb wait-for-device')
	print('Rooting device')
	subprocess.getoutput('adb root')
	bootprompt = False
	unlockprompt = False
	while True:
		layers = findLayers()
		strr = (','.join(layers)).lower()
		if('boot' in strr):
			if(bootprompt == False):
				print('Device is in BootAnim screen')
				bootprompt = True
				unlockprompt = False 
			time.sleep(5)
		elif('navigation' in strr and 'launcher' in strr):
			print('Device is unlocked')
			subprocess.getoutput('adb wait-for-device shell input keyevent 3')
			break
		else:
			if(unlockprompt == False):
				print('Device is locked')
				unlockprompt = True
				bootprompt = False

			subprocess.getoutput('adb wait-for-device shell input keyevent 82')
			subprocess.getoutput('adb wait-for-device shell input keyevent 3')
	subprocess.getoutput("adb wait-for-device shell settings put system screen_off_timeout 72000000")

init()
