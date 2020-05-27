#!python3
from __future__ import print_function
import os
import time
from datetime import datetime

os.system('adb wait-for-device root')
def time_now():
	now=(datetime.now()).strftime('%c')
	now="["+now+"]:"
	return now
while 1:
	print(time_now(),end=" ")
	os.system("adb shell dumpsys SurfaceFlinger | grep \"refresh-rate\"")
	# time.sleep(0.2)
