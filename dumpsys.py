#!python3
from __future__ import print_function
import os
import sys
import subprocess

os.system('adb wait-for-device root')
args = sys.argv
if(len(args)>1 and ('-d' in args or '--d' in args)):
	os.system("adb shell dumpsys SurfaceFlinger > dumpsys.txt")
	exit()
elif(len(args)>1 and 'grep' in args):
	print(args)
	term = args[args.index('grep')+1]
	dump = subprocess.getoutput('adb shell dumpsys SurfaceFlinger').split('\n')
	for line in dump:
		if(term in line):
			print(line)
else:
	os.system('adb shell dumpsys SurfaceFlinger')
input()
