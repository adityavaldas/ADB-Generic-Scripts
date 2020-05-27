#!python3
from __future__ import print_function
import os
import sys
os.system('adb wait-for-device root')
def full_dumpsys():
	while(1):
		os.system("adb shell dumpsys SurfaceFlinger")
		a=input("Enter to continue or Q/q to exit: ")
		if(a.lower()=="q"):
			break
if(len(sys.argv)>1):
	os.system("adb shell dumpsys SurfaceFlinger > dumpsys.txt")
	exit()
full_dumpsys()
