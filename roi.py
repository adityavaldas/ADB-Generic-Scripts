#!python3
import subprocess
import time

def getRoi():
	dumpsys = subprocess.getoutput('adb shell dumpsys SurfaceFlinger').split('\n')
	for line in dumpsys:
		if('ROI(LTRB)' in line):
			print(line)
while True:
	getRoi()
	time.sleep(1)
input()
