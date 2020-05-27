#!python3
import os
import time
from datetime import datetime
os.system('adb wait-for-device root')
def time_now():
	now=(datetime.now()).strftime('%c')
	now="["+now+"]:"
	return now

while 1:
    os.system("adb shell cat /d/dri/0/encoder*/status")
