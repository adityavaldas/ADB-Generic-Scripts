#!python3
import os
os.system('adb wait-for-device root')
os.system("adb shell cat vendor/firmware_mnt/verinfo/ver_info.txt")
input()
