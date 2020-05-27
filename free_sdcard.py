import os
import time
def clearSdcard():
	os.system('adb shell rm -rf sdcard/*.png sdcard/*.jpg sdcard/*.JPG sdcard/*.mp4 sdcard/*.3gp sdcard/*.yuv sdcard/*.avi sdcard/*.MP4 sdcard/*.rgb sdcard/*.raw sdcard/*.mpg sdcard/*.flv sdcard/*.bmp sdcard/*.log')
clearSdcard()
print('Done')
time.sleep(0.6)
