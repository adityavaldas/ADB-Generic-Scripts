#!python3
import os
import subprocess
import re
import sys
import time


dumps = subprocess.getoutput('adb shell dumpsys SurfaceFlinger').split('\n')
for line in dumps:
	if('missed frame count' in line):
		print(line)
