#!python3
import os
import subprocess
import time
os.system('adb wait-for-device root')
while 1:

	listt = subprocess.getoutput('adb shell "cat /sys/kernel/debug/clk/*mdss*/*enable*"').split('\n')
	print(listt)
	time.sleep(0.7)
