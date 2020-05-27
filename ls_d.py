#!python3
from __future__ import print_function
import os
print("Waiting for device")
os.system("adb wait-for-device root")
os.system("adb wait-for-device shell \"ls -lrt /sys/kernel/debug\"")
input()
