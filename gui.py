#!python3
import os
from threading import Thread
import subprocess
try:
	from tkinter import *
except:
	os.system('py -3 -m pip install tkinter')
	from tkinter import *


'''
Init functions
'''

def Tinit():
	Thread(target = init, args = ()).start()

def init():
	killInit = False
	def wake():
		result = subprocess.getoutput("adb shell dumpsys display | grep mScreenState")
		if(result!=None):
			pattern=re.search(r'^.*mScreenState=(\S+)',result)
			state=pattern.group(1)
		if(state==""):
			initT['text'] = "Could not find screenstate, please retry"
		elif(state=="OFF"):
			os.system("adb wait-for-device shell input keyevent 26")
			os.system("adb wait-for-device shell input keyevent 82")
			os.system("adb wait-for-device shell input keyevent 3")
		elif(state=="ON" or "DOZE"):
			os.system("adb wait-for-device shell input keyevent 82")
			os.system("adb wait-for-device shell input keyevent 82")
			os.system("adb wait-for-device shell input keyevent 3")
	def findLayers():
		dumpsys=(subprocess.getoutput(["adb","shell","dumpsys","SurfaceFlinger"]))
		dump_list=dumpsys.split("\n")
		for line_no in range(len(dump_list)):
			if (dump_list[line_no].find("HWC layers:"))>-1:
				first_line=line_no
			if "h/w composer state:" in dump_list[line_no]:
				last_line=line_no
		display_layers_list=dump_list[first_line+1:last_line]

		list = []
		for line in display_layers_list:
			pattern = re.search(r'(.*)\#(.*)',line)
			if(pattern!=None):
				list.append(pattern.group(1).strip())
		return(list)

	initT['text'] = 'Waiting for device'
	os.system('adb wait-for-device')
	initT['text'] = 'Rooting device'
	os.system('adb root')
	initT['text'] = 'Waiting to reach lock screen'

	while True:
		if(killInit == True):
			break
		try:
			os.system('adb wait-for-device shell input keyevent 82')

			layers = findLayers()
			if(len(layers)>1):
				initT['text'] = 'Waking device now'
				wake()
				initT['text'] = 'Setting screen timeout to 20 hours'
				os.system("adb wait-for-device shell settings put system screen_off_timeout 72000000")
				initT['text'] = 'Done'
				killInit = True
				time.sleep(0.5)
				break
		except:
			pass







'''
Devices Window
'''






def devicesWindow():

	def getadbID():
		result=(subprocess.getoutput(["adb","devices"]))
		pattern = re.search(r'^.*(List of devices attached\n)(\S+)\s+(device)', result)
		if(pattern!=None):
			result = pattern.group(2)
		else:
			result = "No devices detected"
		adbDevicesT["text"] = result

	def rootDevice():
		os.system('adb root')
		adbRootT['text'] = 'Rooted the device'
		adbunRootT['text'] = ''

	def unrootDevice():
		os.system('adb unroot')
		adbunRootT['text'] = 'Unrooted the device'
		adbRootT['text'] = ''

	def remountDevice():
		aa = (subprocess.getoutput('adb remount')).split('\n')[-1]
		adbRemountT['text'] = aa

	def disableVerity():
		aa = (subprocess.getoutput('adb disable-verity'))
		adbVerityT['text'] = aa

	def rebootDevice():
		os.system('adb reboot')
		adbRebootT['text'] = 'Rebooted device'

	def quitt():
		devicesW.destroy()

	def adbShell():
		thr = Thread(target = startShell, args = ())
		thr.start()

	def startShell():
		os.system('start adb shell')

	def fb():
		os.system('adb reboot bootloader')



	devicesW = Toplevel(top)
	# devicesW.geometry("1300x700")
	w, h = devicesW.winfo_screenwidth(), devicesW.winfo_screenheight()
	devicesW.geometry("%dx%d+0+0" % (w, h))
	devicesW.title("DEVICES")

	adbDevicesB = Button(devicesW, text='ADB ID', width=30, height = 1, font = ('Calibri', 15, "bold"), command = getadbID, bg = "#229944", fg = "white")
	adbDevicesB.grid(row = 1, column = 0, sticky = "W", padx = 10, pady = 10)
	adbDevicesT = Label(devicesW, text="", font = ('Calibri', 14))
	adbDevicesT.grid(row = 1, column = 1, sticky = "W", padx = 10, pady = 10)

	adbRootB = Button(devicesW, text='ADB ROOT', width=30, height = 1, font = ('Calibri', 15, "bold"), command = rootDevice, bg = "#1199FF", fg = "white")
	adbRootB.grid(row = 2, column = 0, sticky = "W", padx = 10, pady = 10)
	adbRootT = Label(devicesW, text="", font = ('Calibri', 14))
	adbRootT.grid(row = 2, column = 1, sticky = "W", padx = 10, pady = 10)

	adbunRootB = Button(devicesW, text='ADB UNROOT', width=30, height = 1, font = ('Calibri', 15, "bold"), command = unrootDevice, bg = "#1199FF", fg = "white")
	adbunRootB.grid(row = 3, column = 0, sticky = "W", padx = 10, pady = 10)
	adbunRootT = Label(devicesW, text="", font = ('Calibri', 14))
	adbunRootT.grid(row = 3, column = 1, sticky = "W", padx = 10, pady = 10)

	adbRemountB = Button(devicesW, text='ADB REMOUNT', width=30, height = 1, font = ('Calibri', 15, "bold"), command = remountDevice, bg = "#1199FF", fg = "white")
	adbRemountB.grid(row = 4, column = 0, sticky = "W", padx = 10, pady = 10)
	adbRemountT = Label(devicesW, text="", font = ('Calibri', 14))
	adbRemountT.grid(row = 4, column = 1, sticky = "W", padx = 10, pady = 10)

	adbdisableVerityB = Button(devicesW, text='ADB DISABLE VERITY', width=30, height = 1, font = ('Calibri', 15, "bold"), command = disableVerity, bg = "#1199FF", fg = "white")
	adbdisableVerityB.grid(row = 5, column = 0, sticky = "W", padx = 10, pady = 10)
	adbVerityT = Label(devicesW, text="", font = ('Calibri', 14))
	adbVerityT.grid(row = 5, column = 1, sticky = "W", padx = 10, pady = 10)

	adbRebootB = Button(devicesW, text='ADB REBOOT', width=30, height = 1, font = ('Calibri', 15, "bold"), command = rebootDevice, bg = "#1199FF", fg = "white")
	adbRebootB.grid(row = 6, column = 0, sticky = "W", padx = 10, pady = 10)
	adbRebootT = Label(devicesW, text="", font = ('Calibri', 14))
	adbRebootT.grid(row = 6, column = 1, sticky = "W", padx = 10, pady = 10)

	adbShellB = Button(devicesW, text='OPEN ADB SHELL', width=30, height = 1, font = ('Calibri', 15, "bold"), command = adbShell, bg = "#115555", fg = "white")
	adbShellB.grid(row = 7, column = 0, sticky = "W", padx = 10, pady = 10)

	fbB = Button(devicesW, text='SEND TO FASTBOOT', width=30, height = 1, font = ('Calibri', 15, "bold"), command = fb, bg = "#115555", fg = "white")
	fbB.grid(row = 8, column = 0, sticky = "W", padx = 10, pady = 10)

	exitB = Button(devicesW, text='BACK', width=30, height = 1, font = ('Calibri', 15, "bold"),  command = quitt, bg = "#EE1111", fg = "white")
	exitB.grid(row = 0, column = 0, sticky = "W", padx = 10, pady = 10)






'''
Keyevent Window
'''






def keyWindow():
	def quitt():
		keyW.destroy()

	def pressKey(key):
		cmdd = 'adb shell input keyevent '+key
		os.system(cmdd)

	def swipe(dir):
		if(dir == 'up'):
			cmdd = 'adb shell input swipe 500 500 800 200 50'
		elif(dir == 'down'):
			cmdd = 'adb shell input swipe 500 500 200 800 50'
		os.system(cmdd)

	keyW = Toplevel(top)
	# keyW.geometry("1300x700")
	w, h = keyW.winfo_screenwidth(), keyW.winfo_screenheight()
	keyW.geometry("%dx%d+0+0" % (w, h))
	keyW.title('KEYEVENTS')

	exitB = Button(keyW, text='BACK', width=30, height = 1, font = ('Calibri', 15, "bold"), command = quitt, bg = "#EE1111", fg = "white")
	exitB.grid(row = 0, column = 0, sticky = "W", padx = 10, pady = 10)

	press26B = Button(keyW, text='POWER BUTTON', width=30, height = 1, font = ('Calibri', 15, "bold"), command = lambda: pressKey('26'), bg = "#44BB55", fg = "white")
	press26B.grid(row = 1, column = 0, sticky = "W", padx = 10, pady = 10)

	press82B = Button(keyW, text='HOME BUTTON', width=30, height = 1, font = ('Calibri', 15, "bold"), command = lambda: pressKey('3'), bg = "#44BB55", fg = "white")
	press82B.grid(row = 2, column = 0, sticky = "W", padx = 10, pady = 10)

	press82B = Button(keyW, text='MENU BUTTON', width=30, height = 1, font = ('Calibri', 15, "bold"), command = lambda: pressKey('82'), bg = "#44BB55", fg = "white")
	press82B.grid(row = 3, column = 0, sticky = "W", padx = 10, pady = 10)

	press82B = Button(keyW, text='BACK BUTTON', width=30, height = 1, font = ('Calibri', 15, "bold"), command = lambda: pressKey('4'), bg = "#44BB55", fg = "white")
	press82B.grid(row = 4, column = 0, sticky = "W", padx = 10, pady = 10)

	press82B = Button(keyW, text='VOLUME UP', width=30, height = 1, font = ('Calibri', 15, "bold"), command = lambda: pressKey('24'), bg = "#44BB55", fg = "white")
	press82B.grid(row = 1, column = 2, sticky = "W", padx = 10, pady = 10)

	press82B = Button(keyW, text='VOLUME DOWN', width=30, height = 1, font = ('Calibri', 15, "bold"), command = lambda: pressKey('25'), bg = "#44BB55", fg = "white")
	press82B.grid(row = 2, column = 2, sticky = "W", padx = 10, pady = 10)

	press82B = Button(keyW, text='SWIPE UP', width=30, height = 1, font = ('Calibri', 15, "bold"), command = lambda: swipe('up'), bg = "#44BB55", fg = "white")
	press82B.grid(row = 1, column = 1, sticky = "W", padx = 10, pady = 10)

	press82B = Button(keyW, text='SWIPE DOWN', width=30, height = 1, font = ('Calibri', 15, "bold"), command = lambda: swipe('down'), bg = "#44BB55", fg = "white")
	press82B.grid(row = 2, column = 1, sticky = "W", padx = 10, pady = 10)







'''
Shell Stop/Start Window
'''






def shellWindow():
	def quitt():
		shellW.destroy()

	def shell(act):
		cmdd = 'adb shell '+ act
		os.system(cmdd)

	def composer(act):
		cmdd = 'adb shell '+ act
		os.system(cmdd)
		cmdd = 'adb shell '+ act + ' vendor.hwcomposer-2-2'
		os.system(cmdd)
		cmdd = 'adb shell '+ act + ' vendor.qti.hardware.display.composer'
		os.system(cmdd)


	shellW = Toplevel(top)
	# shellW.geometry("1300x700")
	w, h = shellW.winfo_screenwidth(), shellW.winfo_screenheight()
	shellW.geometry("%dx%d+0+0" % (w, h))
	shellW.title('SHELL STOP/START')

	quitB = Button(shellW, text='BACK', width=30, height = 1, font = ('Calibri', 15, "bold"), command = quitt, bg = "#EE1111", fg = "white")
	quitB.grid(row = 0, column = 0, sticky = "W", padx = 10, pady = 10)

	sstopB = Button(shellW, text='SHELL STOP', width=30, height = 1, font = ('Calibri', 15, "bold"), command = lambda: shell('stop'), bg = "#EE1111", fg = "white")
	sstopB.grid(row = 1, column = 0, sticky = "W", padx = 10, pady = 10)

	sstartB = Button(shellW, text='SHELL START', width=30, height = 1, font = ('Calibri', 15, "bold"), command = lambda: shell('start'), bg = "#44BB55", fg = "white")
	sstartB.grid(row = 2, column = 0, sticky = "W", padx = 10, pady = 10)

	cstopB = Button(shellW, text='COMPOSER STOP', width=30, height = 1, font = ('Calibri', 15, "bold"), command = lambda: composer('stop'), bg = "#EE1111", fg = "white")
	cstopB.grid(row = 3, column = 0, sticky = "W", padx = 10, pady = 10)

	cstartB = Button(shellW, text='COMPOSER START', width=30, height = 1, font = ('Calibri', 15, "bold"), command = lambda: composer('start'), bg = "#44BB55", fg = "white")
	cstartB.grid(row = 4, column = 0, sticky = "W", padx = 10, pady = 10)






'''
Dumpsys Window
'''






def dumpsysWindow():
	global findRRFlag
	findRRFlag = False

	def quitt():
		dumpsysW.destroy()

	def writeDumpsys():
		with open('dumpsys.txt' ,'w') as f:
			try:
				f.write(subprocess.getoutput('adb shell dumpsys SurfaceFlinger'))
				toTextT['text'] = 'Wrote to dumpsys.txt in current directory'
			except:
				toTextT['text'] = 'Failed, please try again'

	def findRes():
		getResT['text'] = subprocess.getoutput('adb shell wm size').split(':')[-1]

	def findFps():
		string = ''
		output = subprocess.getoutput('adb shell dumpsys SurfaceFlinger').split('\n')
		for line in output:
			pattern = re.search(r'^(.*)fps:(.*)',line)
			if(pattern!=None):
				string = string + pattern.group(1)+','
		getFpsT['text'] = string[:-1]

	def findLayers():
		dumpsys=(subprocess.getoutput(["adb","shell","dumpsys","SurfaceFlinger"]))
		dump_list=dumpsys.split("\n")
		for line_no in range(len(dump_list)):
			if (dump_list[line_no].find("HWC layers:"))>-1:
				first_line=line_no
			if "h/w composer state:" in dump_list[line_no]:
				last_line=line_no
		display_layers_list=dump_list[first_line+1:last_line]
		strr = ""
		for line in display_layers_list:
			strr = strr + line + '\n'
		consoleT['text'] = strr

	def findComp():
		dumpsys=subprocess.getoutput(["adb","shell","dumpsys","SurfaceFlinger"])
		dump_list=dumpsys.split("\n")
		for line_no in range(len(dump_list)):
			if dump_list[line_no].find("Idx")>-1:
				first_line=line_no
			if "Allocated buffers" in dump_list[line_no]:
				last_line=line_no
		display_comp_list=dump_list[first_line:last_line]
		strr = ''
		for line in display_comp_list:
			strr = strr + line +'\n'
		consoleT['text'] = strr

	def findRR():
		global findRRFlag
		findRRFlag = not findRRFlag
		Thread(target = tFindRR, args = ()).start()

	def tFindRR():
		while True:
			global findRRFlag
			if(findRRFlag == True):
				strr = subprocess.getoutput('adb shell dumpsys SurfaceFlinger | grep refresh-rate')
				getRRT['text'] = strr
			if(findRRFlag == False):
				getRRT['text'] = ''
				break

	def findRoi():
		result = subprocess.getoutput('adb shell dumpsys SurfaceFlinger | grep ROI(LTRB)')
		getRoiT['text'] = result


	dumpsysW = Toplevel(top)
	# dumpsysW.geometry("1300x700")
	w, h = dumpsysW.winfo_screenwidth(), dumpsysW.winfo_screenheight()
	dumpsysW.geometry("%dx%d+0+0" % (w, h))
	dumpsysW.title('DUMPSYS')

	toTextB = Button(dumpsysW, text='WRITE DUMPSYS TO TEXT FILE', width=30, height = 1, font = ('Calibri', 15, "bold"), command = writeDumpsys, bg = "#1199FF", fg = "white")
	toTextB.grid(row = 1, column = 0, sticky = "W", padx = 10, pady = 10)
	toTextT = Label(dumpsysW, text="", font = ('Calibri', 14), justify = 'left')
	toTextT.grid(row = 1, column = 1, sticky = "W", padx = 10, pady = 10)

	getResB = Button(dumpsysW, text='RESOLUTION', width=30, height = 1, font = ('Calibri', 15, "bold"), command = findRes, bg = "#1199FF", fg = "white")
	getResB.grid(row = 2, column = 0, sticky = "W", padx = 10, pady = 10)
	getResT = Label(dumpsysW, text="", font = ('Calibri', 14), justify = 'left')
	getResT.grid(row = 2, column = 1, sticky = "W", padx = 10, pady = 10)

	getFpsB = Button(dumpsysW, text='SUPPORTED FPS', width=30, height = 1, font = ('Calibri', 15, "bold"), command = findFps, bg = "#44BB55", fg = "white")
	getFpsB.grid(row = 3, column = 0, sticky = "W", padx = 10, pady = 10)
	getFpsT = Label(dumpsysW, text="", font = ('Calibri', 14), justify = 'left')
	getFpsT.grid(row = 3, column = 1, sticky = "W", padx = 10, pady = 10)

	getRRB = Button(dumpsysW, text='CURRENT FPS', width=30, height = 1, font = ('Calibri', 15, "bold"), command = findRR, bg = "#44BB55", fg = "white")
	getRRB.grid(row = 4, column = 0, sticky = "W", padx = 10, pady = 10)
	getRRT = Label(dumpsysW, text="", font = ('Calibri', 14), justify = 'left')
	getRRT.grid(row = 4, column = 1, sticky = "W", padx = 10, pady = 10)


	getLayersB = Button(dumpsysW, text='LAYERS INFO', width=30, height = 1, font = ('Calibri', 15, "bold"), command = findLayers, bg = "#115555", fg = "white")
	getLayersB.grid(row = 5, column = 0, sticky = "W", padx = 10, pady = 10)

	getCompB = Button(dumpsysW, text='COMPOSITION INFO', width=30, height = 1, font = ('Calibri', 15, "bold"), command = findComp, bg = "#115555", fg = "white")
	getCompB.grid(row = 6, column = 0, sticky = "W", padx = 10, pady = 10)

	getRoiB = Button(dumpsysW, text='ROI', width=30, height = 1, font = ('Calibri', 15, "bold"), command = findRoi, bg = "#DDDD44", fg = "white")
	getRoiB.grid(row = 7, column = 0, sticky = "W", padx = 10, pady = 10)
	getRoiT = Label(dumpsysW, text="", font = ('Calibri', 14))
	getRoiT.grid(row = 7, column = 1, sticky = "W", padx = 10, pady = 10)

	consoleT = Label(dumpsysW, text="", font = ('Calibri', 14), justify = 'left')
	consoleT.grid(row = 8, column = 0, rowspan = 4, sticky = "W", padx = 10, pady = 10)

	exitB = Button(dumpsysW, text='BACK', width=30, height = 1, font = ('Calibri', 15, "bold"), command = quitt, bg = "#EE1111", fg = "white")
	exitB.grid(row = 0, column = 0, sticky = "W", padx = 10, pady = 10)






'''
Logging Window
'''





def loggingWindow():

	global lcFlag
	global krFlag
	lcFlag = krFlag = False
	def quitt():
		logW.destroy()

	def tcollectLogcat():
		Thread(target = collectLogcat, args = ()).start()

	def collectLogcat():
		global lcFlag
		if(lcFlag == False):

			lcB['text'] = 'STOP LOGCAT'
			lcB['bg'] = '#AA4444'
			lcFlag = True
			os.system('start "logcatt" adb shell logcat | tee logcat.txt')
		elif(lcFlag == True):
			lcB['text'] = 'START LOGCAT'
			lcB['bg'] = '#11AA99'
			output = subprocess.getoutput('tasklist /v /fo csv | findstr /i logcatt').split(",")[1][1:-1]
			if(output):
				cmdd = "taskkill /PID "+output
				os.system(cmdd)
			lcFlag = False

	def clearLogcat():
		os.system('adb shell logcat -c')

	def tcollectKernel():
		Thread(target = collectKernel, args = ()).start()

	def collectKernel():
		global krFlag
		if(krFlag == False):

			krB['text'] = 'STOP KERNEL'
			krFlag = True
			krB['bg'] = '#AA4444'
			os.system('start "kernell" adb shell logcat -b kernel | tee kernellog.txt')
		elif(krFlag == True):
			krB['text'] = 'START KERNEL'
			krB['bg'] = '#11AA99'
			output = subprocess.getoutput('tasklist /v /fo csv | findstr /i kernell').split(",")[1][1:-1]
			if(output):
				cmdd = "taskkill /PID "+output
				os.system(cmdd)
			krFlag = False

	def clearKernel():
		os.system('adb shell logcat -b kernel -c')

	def tcollectSystrace():
		Thread(target = collectSystrace, args = ()).start()

	def collectSystrace():
		dur = systraceE.get()
		if(dur!=None):
			cmdd = r'start "systrace" py -2 \\cube\Android_DisplayAutomation\Python\systrace\systrace.py -t ' + dur + ' -b 64000 -o trace.html'
			os.system(cmdd)

	def clearLogs():
		tr = ['kernellog.txt','logcat.txt','trace.html']
		for file in tr:
			try:
				os.remove(file)
			except:
				pass

	logW = Toplevel(top)
	w, h = logW.winfo_screenwidth(), logW.winfo_screenheight()
	logW.geometry("%dx%d+0+0" % (w, h))
	logW.title('LOGGING')
	# logW.geometry("1300x700")

	quitB = Button(logW, text='BACK', width=30, height = 1, font = ('Calibri', 15, "bold"),  command = quitt, bg = "#EE1111", fg = "white")
	quitB.grid(row = 0, column = 0, sticky = "W", padx = 10, pady = 10)

	lcB = Button(logW, text='START LOGCAT', width=30, height = 1, font = ('Calibri', 15, "bold"), command = tcollectLogcat, bg = "#11AA99", fg = "white")
	lcB.grid(row = 1, column = 0, sticky = "W", padx = 10, pady = 10)
	lcT = Label(logW, text="", font = ('Calibri', 14))
	lcT.grid(row = 1, column = 1, sticky = "W", padx = 10, pady = 10)

	krB = Button(logW, text='START KERNEL', width=30, height = 1, font = ('Calibri', 15, "bold"), command = tcollectKernel, bg = "#11AA99", fg = "white")
	krB.grid(row = 2, column = 0, sticky = "W", padx = 10, pady = 10)
	krT = Label(logW, text="", font = ('Calibri', 14))
	krT.grid(row = 2, column = 1, sticky = "W", padx = 10, pady = 10)

	lccB = Button(logW, text='CLEAR LOGCAT', width=30, height = 1, font = ('Calibri', 15, "bold"), command = clearLogcat, bg = "#999999", fg = "white")
	lccB.grid(row = 3, column = 0, sticky = "W", padx = 10, pady = 10)

	krcB = Button(logW, text='CLEAR KERNEL', width=30, height = 1, font = ('Calibri', 15, "bold"), command = clearKernel, bg = "#999999", fg = "white")
	krcB.grid(row = 4, column = 0, sticky = "W", padx = 10, pady = 10)

	systraceB = Button(logW, text='RUN SYSTRACE, DUR -->', width=30, height = 1, font = ('Calibri', 15, "bold"), command = tcollectSystrace, bg = "#11AA99", fg = "white")
	systraceB.grid(row = 5, column = 0, sticky = "W", padx = 10, pady = 10)

	systraceE = Entry(logW, bd = 3, font = ('Calibri', 15), bg = "#666666", fg = "#FFFFFF")
	systraceE.insert(0, "30")
	systraceE.grid(row = 5, column = 1, sticky = "W", padx = 10, pady = 10)

	clrB = Button(logW, text='CLEAR COLLECTED LOGS', width=30, height = 1, font = ('Calibri', 15, "bold"), command = clearLogs, bg = "#444444", fg = "white")
	clrB.grid(row = 6, column = 0, sticky = "W", padx = 10, pady = 10)






'''
Launch Apps Window
'''






def launchAppWindow():
	def quitt():
		appW.destroy()

	def gears():
		installed = False
		result = subprocess.getoutput('adb shell pm list packages').splitlines()
		for line in result:
			if('gears' in line):
				installed = True
		if(installed == False):
			cmdd = r'adb install \\cube\Android_DisplayAutomation\APK\base.apk'
			os.system(cmdd)
		os.system('adb shell am start -a android.intent.action.MAIN -n com.jeffboody.GearsES2eclair/.GearsES2eclair')

	def mx():
		installed = False
		result = subprocess.getoutput('adb shell pm list packages').splitlines()
		for line in result:
			if('mxlauncher' in line):
				installed = True
		if(installed == False):
			cmdd = r'adb install \\cube\Android_DisplayAutomation\APK\MxLauncher3D.apk'
			os.system(cmdd)
		os.system('adb shell am start -a android.intent.category.LAUNCHER -n com.samsung.testapp.mxlauncher3d/.MxLauncher3D')

	def tl():
		installed = False
		result = subprocess.getoutput('adb shell pm list packages').splitlines()
		for line in result:
			if('touchlatency' in line):
				installed = True
		if(installed == False):
			cmdd = r'adb install \\cube\Android_DisplayAutomation\Python\UIBench\bin\TouchLatency-90fps.apk'
			os.system(cmdd)
		cmdd = r'START /B adb shell "am instrument -w -r -e iterations 1000 -e class "com.android.wearable.touch.janktests.BouncingBallJankTest#testBouncingBall" com.android.wearable.touch.janktests/android.test.InstrumentationTestRunner" > nul'
		os.system(cmdd)

	def mw():
		installed = False
		result = subprocess.getoutput('adb shell pm list packages').splitlines()
		for line in result:
			if('qualcomm.multiple_windows' in line):
				installed = True
		if(installed == False):
			cmdd = r'adb install \\cube\Android_DisplayAutomation\APK\Multiple_Windows.apk'
			os.system(cmdd)
		cmdd = r'adb shell am start -a android.intent.category.LAUNCHER -n com.qualcomm.multiple_windows/.MainActivity'
		os.system(cmdd)

	appW = Toplevel(top)
	w, h = appW.winfo_screenwidth(), appW.winfo_screenheight()
	appW.geometry("%dx%d+0+0" % (w, h))
	# appW.geometry("1300x700")
	appW.title('LAUNCH APP')
	quitB = Button(appW, text='BACK', width=30, height = 1, font = ('Calibri', 15, "bold"),  command = quitt, bg = "#EE1111", fg = "white")
	quitB.grid(row = 0, column = 0, sticky = "W", padx = 10, pady = 10)

	gearsB = Button(appW, text='GEARS', width=30, height = 1, font = ('Calibri', 15, "bold"), command = gears, bg = "#1199FF", fg = "white")
	gearsB.grid(row = 1, column = 0, sticky = "W", padx = 10, pady = 10)
	gearsT = Label(appW, text="", font = ('Calibri', 14))
	gearsT.grid(row = 1, column = 1, sticky = "W", padx = 10, pady = 10)

	mxB = Button(appW, text='MXLAUNCHER3D', width=30, height = 1, font = ('Calibri', 15, "bold"), command = mx, bg = "#1199FF", fg = "white")
	mxB.grid(row = 2, column = 0, sticky = "W", padx = 10, pady = 10)
	mxT = Label(appW, text="", font = ('Calibri', 14))
	mxT.grid(row = 2, column = 1, sticky = "W", padx = 10, pady = 10)

	tlB = Button(appW, text='TOUCHLATENCY', width=30, height = 1, font = ('Calibri', 15, "bold"), command = tl, bg = "#1199FF", fg = "white")
	tlB.grid(row = 3, column = 0, sticky = "W", padx = 10, pady = 10)
	tlT = Label(appW, text="", font = ('Calibri', 14))
	tlT.grid(row = 3, column = 1, sticky = "W", padx = 10, pady = 10)

	tlB = Button(appW, text='MULTIPLE WINDOWS', width=30, height = 1, font = ('Calibri', 15, "bold"), command = mw, bg = "#1199FF", fg = "white")
	tlB.grid(row = 4, column = 0, sticky = "W", padx = 10, pady = 10)
	tlT = Label(appW, text="", font = ('Calibri', 14))
	tlT.grid(row = 4, column = 1, sticky = "W", padx = 10, pady = 10)






'''
Clocks Gating or Not
'''





def clocks():
	Thread(target = tClocks, args = ()).start()

def tClocks():
	while True:
		no = 0
		result = subprocess.getoutput('adb shell \"cat /sys/kernel/debug/clk/*mdss*/*enable*\"').splitlines()
		if(result!=None):
			for item in result:
				item = int(item)
				no+=item
			strr = 'ACTIVE CLOCKS: ' + str(no)
			clkB['text'] = strr
		else:
			clkB['text'] = 'CLOCKS'



'''
Video Playback Window
'''





def videoPlayback():

	def quitt():
		videoW.destroy()

	def Tvid(video):
		Thread(target = vid, args = (video,)).start()

	def vid(video):
		foundVideo = False
		sdcardContents = subprocess.getoutput('adb shell ls sdcard').splitlines()
		for item in sdcardContents:
			if(video in item):
				foundVideo = True
				break
		if(foundVideo == False):
			cmdd = 'adb push \\\\cube\\Android_DisplayAutomation\\TestContents\\Videos\\' + video + ' sdcard'
			os.system(cmdd)
		cmdd = 'adb wait-for-device shell am start -n org.codeaurora.gallery/com.android.gallery3d.app.MovieActivity -d /sdcard/' + video+' -t "video/*"'
		os.system(cmdd)

	videoW = Toplevel(top)
	videoW.title('Video Playback')
	w, h = videoW.winfo_screenwidth(), videoW.winfo_screenheight()
	videoW.geometry("%dx%d+0+0" % (w, h))
	# videoW.geometry("1300x700")

	quitB = Button(videoW, text='BACK', width=30, height = 1, font = ('Calibri', 15, "bold"),  command = quitt, bg = "#EE1111", fg = "white")
	quitB.grid(row = 0, column = 0, sticky = "W", padx = 10, pady = 10)

	v1080pB = Button(videoW, text='1080p', width=30, height = 1, font = ('Calibri', 15, "bold"), command = lambda: Tvid('Qtc88.mp4'), bg = "#1199FF", fg = "white")
	v1080pB.grid(row = 1, column = 0, sticky = "W", padx = 10, pady = 10)

	v720pB = Button(videoW, text='720p', width=30, height = 1, font = ('Calibri', 15, "bold"), command = lambda: Tvid('Qtc_720.mp4'), bg = "#1199FF", fg = "white")
	v720pB.grid(row = 2, column = 0, sticky = "W", padx = 10, pady = 10)

	vfastB = Button(videoW, text='FWVGA_H264', width=30, height = 1, font = ('Calibri', 15, "bold"), command = lambda: Tvid('05-fastfurious_FWVGA_H264.3gp'), bg = "#1199FF", fg = "white")
	vfastB.grid(row = 3, column = 0, sticky = "W", padx = 10, pady = 10)

	v640B = Button(videoW, text='640x480, 24FPS', width=30, height = 1, font = ('Calibri', 15, "bold"), command = lambda: Tvid('Avatar_Trailer_H.263_mp4_BR=0.37Mbps_640x480_FPS=24_BD=8bits_AAC-LC_BR=128kbps_SR=48KHz.mp4'), bg = "#1199FF", fg = "white")
	v640B.grid(row = 4, column = 0, sticky = "W", padx = 10, pady = 10)

	v2kB = Button(videoW, text='2160p, 30FPS', width=30, height = 1, font = ('Calibri', 15, "bold"), command = lambda: Tvid('cornell_2160p_H264_HP5_30fps_3Mbps_AAC_192kbps_45s.mp4'), bg = "#1199FF", fg = "white")
	v2kB.grid(row = 5, column = 0, sticky = "W", padx = 10, pady = 10)

	v2kB = Button(videoW, text='QVGA, 30FPS', width=30, height = 1, font = ('Calibri', 15, "bold"), command = lambda: Tvid('freeriders_QVGA_H_264_1Mbps_30fps.mp4'), bg = "#1199FF", fg = "white")
	v2kB.grid(row = 6, column = 0, sticky = "W", padx = 10, pady = 10)

	v2kB = Button(videoW, text='4128x2240', width=30, height = 1, font = ('Calibri', 15, "bold"), command = lambda: Tvid('H264_4128x2240_MP3.flv'), bg = "#1199FF", fg = "white")
	v2kB.grid(row = 7, column = 0, sticky = "W", padx = 10, pady = 10)

	v2kB = Button(videoW, text='Hobbit', width=30, height = 1, font = ('Calibri', 15, "bold"), command = lambda: Tvid('hobbit.mp4'), bg = "#1199FF", fg = "white")
	v2kB.grid(row = 0, column = 1, sticky = "W", padx = 10, pady = 10)

	v2kB = Button(videoW, text='Inception', width=30, height = 1, font = ('Calibri', 15, "bold"), command = lambda: Tvid('Inception.3gp'), bg = "#1199FF", fg = "white")
	v2kB.grid(row = 1, column = 1, sticky = "W", padx = 10, pady = 10)

	v2kB = Button(videoW, text='4096x2160, 24FPS', width=30, height = 1, font = ('Calibri', 15, "bold"), command = lambda: Tvid('Mobscene4096_2160_100_24fps_50s.mp4'), bg = "#1199FF", fg = "white")
	v2kB.grid(row = 2, column = 1, sticky = "W", padx = 10, pady = 10)

	v2kB = Button(videoW, text='3840x2160, 30FPS, QCOM', width=30, height = 1, font = ('Calibri', 15, "bold"), command = lambda: Tvid('QCOM_1_AAC_8_3840x2160_30fps_40Mbps.mp4'), bg = "#1199FF", fg = "white")
	v2kB.grid(row = 3, column = 1, sticky = "W", padx = 10, pady = 10)

	v2kB = Button(videoW, text='SAMSUNG HDR WONDERLAND', width=30, height = 1, font = ('Calibri', 15, "bold"), command = lambda: Tvid('Samsung_HDR_Wonderland.mp4'), bg = "#1199FF", fg = "white")
	v2kB.grid(row = 4, column = 1, sticky = "W", padx = 10, pady = 10)

	v2kB = Button(videoW, text='3840x2160, 30FPS, SPEEDBOAT', width=30, height = 1, font = ('Calibri', 15, "bold"), command = lambda: Tvid('Speedboat_h264_3840x2160_30fps_42mbps_45s_AV.mp4'), bg = "#1199FF", fg = "white")
	v2kB.grid(row = 5, column = 1, sticky = "W", padx = 10, pady = 10)

	v2kB = Button(videoW, text='ITUHLG', width=30, height = 1, font = ('Calibri', 15, "bold"), command = lambda: Tvid('St_1000_60p_ITUHLG_2020_au.mp4'), bg = "#1199FF", fg = "white")
	v2kB.grid(row = 6, column = 1, sticky = "W", padx = 10, pady = 10)

	v2kB = Button(videoW, text='HDR10+', width=30, height = 1, font = ('Calibri', 15, "bold"), command = lambda: Tvid('teststream_HDR10+_v04_30Hz.mp4'), bg = "#1199FF", fg = "white")
	v2kB.grid(row = 7, column = 1, sticky = "W", padx = 10, pady = 10)

	v2kB = Button(videoW, text='VGA, 25FPS', width=30, height = 1, font = ('Calibri', 15, "bold"), command = lambda: Tvid('UR-MP4_VGA_25fps_185Kbps_MP3_44.1KHz_128Kbps.mp4'), bg = "#1199FF", fg = "white")
	v2kB.grid(row = 0, column = 2, sticky = "W", padx = 10, pady = 10)

	v2kB = Button(videoW, text='1280x720, 30FPS', width=30, height = 1, font = ('Calibri', 15, "bold"), command = lambda: Tvid('VideosWEBM_VP8_1280x720_10000kbps_30fps.webm'), bg = "#1199FF", fg = "white")
	v2kB.grid(row = 1, column = 2, sticky = "W", padx = 10, pady = 10)






'''
Rotate Window
'''





def rotateWindow():
	def quitt():
		rotW.destroy()

	def rotate(angle):
		os.system('adb shell settings put system accelerometer_rotation 0')
		cmdd = 'adb shell settings put system user_rotation ' + angle
		os.system(cmdd)

	rotW = Toplevel(top)
	rotW.title('BUILD ON DUT')
	w, h = rotW.winfo_screenwidth(), rotW.winfo_screenheight()
	rotW.geometry("%dx%d+0+0" % (w, h))
	# rotW.geometry("1300x700")

	quitB = Button(rotW, text='BACK', width=30, height = 1, font = ('Calibri', 15, "bold"),  command = quitt, bg = "#EE1111", fg = "white")
	quitB.grid(row = 0, column = 0, sticky = "W", padx = 10, pady = 10)

	r0 = Button(rotW, text='0', width=30, height = 1, font = ('Calibri', 15, "bold"), command = lambda: rotate('0'), bg = "#1199FF", fg = "white")
	r0.grid(row = 1, column = 0, sticky = "W", padx = 10, pady = 10)

	r1 = Button(rotW, text='90', width=30, height = 1, font = ('Calibri', 15, "bold"), command = lambda: rotate('1'), bg = "#1199FF", fg = "white")
	r1.grid(row = 2, column = 0, sticky = "W", padx = 10, pady = 10)

	r2 = Button(rotW, text='180', width=30, height = 1, font = ('Calibri', 15, "bold"), command = lambda: rotate('2'), bg = "#1199FF", fg = "white")
	r2.grid(row = 3, column = 0, sticky = "W", padx = 10, pady = 10)

	r3 = Button(rotW, text='270', width=30, height = 1, font = ('Calibri', 15, "bold"), command = lambda: rotate('3'), bg = "#1199FF", fg = "white")
	r3.grid(row = 4, column = 0, sticky = "W", padx = 10, pady = 10)








'''
Panel on DUT Window
'''







'''
Build on DUT Window
'''
def panelDetails():

	def quitt():
		panelW.destroy()

	panelW = Toplevel(top)
	panelW.title('BUILD ON DUT')
	# w, h = panelW.winfo_screenwidth(), panelW.winfo_screenheight()
	# panelW.geometry("%dx%d+0+0" % (w, h))
	panelW.geometry("500x100")
	files = subprocess.getoutput('adb shell ls d').split()
	for file in files:
		if('vid' in file or 'cmd' in file):
			cmdd = 'adb shell ls d/' + file
			file_contents = subprocess.getoutput(cmdd).split()
			for item in file_contents:
				if('esd_trigger' in item):
					panel_file = file
	tlabel = Label(panelW, text="", font = ('Calibri', 14), anchor = 'w', justify = 'left')
	tlabel.grid(row = 4, column = 1, sticky = "W", padx = 10, pady = 10, rowspan = 10)
	tlabel['text'] = panel_file


def buildDetails():

	def quitt():
		buildW.destroy()

	buildW = Toplevel(top)
	buildW.title('BUILD ON DUT')
	# w, h = buildW.winfo_screenwidth(), buildW.winfo_screenheight()
	# buildW.geometry("%dx%d+0+0" % (w, h))
	buildW.geometry("1300x700")

	tlabel = Label(buildW, text="", font = ('Calibri', 14), anchor = 'w', justify = 'left')
	tlabel.grid(row = 4, column = 1, sticky = "W", padx = 10, pady = 10, rowspan = 10)

	result = subprocess.getoutput('adb root && adb shell cat vendor/firmware_mnt/verinfo/ver_info.txt')
	tlabel['text'] = result






'''
Clear SDCARD
'''




def clearSdcard():
	os.system('adb shell rm -rf sdcard/*.png sdcard/*.jpg sdcard/*.JPG sdcard/*.mp4 sdcard/*.3gp sdcard/*.yuv sdcard/*.avi sdcard/*.MP4 sdcard/*.rgb sdcard/*.raw sdcard/*.mpg sdcard/*.flv sdcard/*.bmp sdcard/*.log')





'''
build Window
'''





def buildWindow():

	def quitt():
		buildW.destroy()


	def tbuildd(prod):
		consoleT['text'] = 'Please wait for upto 30 seconds'
		Thread(target = buildd, args = (prod,)).start()

	def buildd(prod):
		# files = subprocess.getoutput('ls \\\\crmhyd\\nsid-hyd-05 | grep "Agatti"').split('\n')
		files = subprocess.getoutput('time/T')
		strr = ''
		for file in files:
			strr = strr + file + '\n'

		consoleT['text'] = 'Done'

		frameW = Toplevel(buildW)
		frameW.title(prod)
		# w, h = frameW.winfo_screenwidth(), frameW.winfo_screenheight()
		# frameW.geometry("%dx%d+0+0" % (w, h))
		frameW.geometry("1300x700")

		tlabel = Text(frameW, text="", font = ('Calibri', 14), anchor = 'w', justify = 'left')
		tlabel.grid(row = 0, column = 0, sticky = "W", padx = 10, pady = 10, rowspan = 10)
		tlabel['text'] = strr
		tlabel.configure(state = 'disable')

	buildW = Toplevel(top)
	buildW.title('AVAILABLE BUILDS')
	w, h = buildW.winfo_screenwidth(), buildW.winfo_screenheight()
	buildW.geometry("%dx%d+0+0" % (w, h))
	# buildW.geometry("1300x700")

	quitB = Button(buildW, text='BACK', width=30, height = 1, font = ('Calibri', 15, "bold"),  command = quitt, bg = "#EE1111", fg = "white")
	quitB.grid(row = 0, column = 0, sticky = "W", padx = 10, pady = 10)

	agattiB = Button(buildW, text='AGATTI', width=30, height = 1, font = ('Calibri', 15, "bold"),  command = lambda: tbuildd('Agatti'), bg = "#44BB55", fg = "white")
	agattiB.grid(row = 1, column = 0, sticky = "W", padx = 10, pady = 10)

	consoleT = Label(buildW, text="", font = ('Calibri', 14), justify = 'left')
	consoleT.grid(row = 6, column = 0, sticky = "W", padx = 10, pady = 10)





'''
ESD Trigger
'''



def esdTrigger():
	files = subprocess.getoutput('adb shell ls d').split()
	for file in files:
		if('vid' in file or 'cmd' in file):
			cmdd = 'adb shell ls d/' + file
			file_contents = subprocess.getoutput(cmdd).split()
			for item in file_contents:
				if('esd_trigger' in item):
					panel_file = file

	cmdd = 'adb shell "echo -n 1 > /d/' + panel_file + '/esd_trigger"'
	os.system(cmdd)






'''
PP Window
'''





def ppWindow():

	def quitt():
		ppW.destroy()

	def ppd(feat, status):
		cmdd = 'adb shell ppd ' + feat + ':' + status
		if(feat == 'Ltm'):
			cmdd = 'adb shell ppd ' + feat + ':' + status + ':Primary:Auto'
		result = subprocess.getoutput(cmdd)
		consoleT['text'] = result
		if(feat == 'foss'):
			result = subprocess.getoutput('adb shell ppd als:input:500')
		consoleT['text'] = result

	def als():
		result = subprocess.getoutput('adb shell ppd Ltm:Als:Primary:500')
		result = subprocess.getoutput('adb shell ppd Ltm:Als:Primary:1000')
		consoleT['text'] = result

	def status(feat):
		cmdd = 'adb shell ppd ' + feat + ':status'
		if(feat == 'Ltm'):
			cmdd = 'adb shell ppd ' + feat + ':Status:Primary'
		result = subprocess.getoutput(cmdd)
		consoleT['text'] = result

	ppW = Toplevel(top)
	ppW.title('POST PROCESSING')
	w, h = ppW.winfo_screenwidth(), ppW.winfo_screenheight()
	ppW.geometry("%dx%d+0+0" % (w, h))
	# ppW.geometry("1300x700")

	quitB = Button(ppW, text='BACK', width=30, height = 1, font = ('Calibri', 15, "bold"),  command = quitt, bg = "#EE1111", fg = "white")
	quitB.grid(row = 0, column = 0, sticky = "W", padx = 10, pady = 10)

	sviOnB = Button(ppW, text='SVI ON', width=30, height = 1, font = ('Calibri', 15, "bold"),  command = lambda: ppd('svi','on'), bg = "#44BB55", fg = "white")
	sviOnB.grid(row = 1, column = 0, sticky = "W", padx = 10, pady = 10)

	sviOffB = Button(ppW, text='SVI OFF', width=30, height = 1, font = ('Calibri', 15, "bold"),  command = lambda: ppd('svi','off'), bg = "#DD8888", fg = "white")
	sviOffB.grid(row = 2, column = 0, sticky = "W", padx = 10, pady = 10)

	svisB = Button(ppW, text='SVI STATUS', width=30, height = 1, font = ('Calibri', 15, "bold"),  command = lambda: status('svi'), bg = "#1199FF", fg = "white")
	svisB.grid(row = 3, column = 0, sticky = "W", padx = 10, pady = 10)

	cablOnB = Button(ppW, text='CABL ON', width=30, height = 1, font = ('Calibri', 15, "bold"),  command = lambda: ppd('cabl','on'), bg = "#44BB55", fg = "white")
	cablOnB.grid(row = 1, column = 1, sticky = "W", padx = 10, pady = 10)

	cablOffB = Button(ppW, text='CABL OFF', width=30, height = 1, font = ('Calibri', 15, "bold"),  command = lambda: ppd('cabl','off'), bg = "#DD8888", fg = "white")
	cablOffB.grid(row = 2, column = 1, sticky = "W", padx = 10, pady = 10)

	cablsB = Button(ppW, text='CABL STATUS', width=30, height = 1, font = ('Calibri', 15, "bold"),  command = lambda: status('cabl'), bg = "#1199FF", fg = "white")
	cablsB.grid(row = 3, column = 1, sticky = "W", padx = 10, pady = 10)

	fossOnB = Button(ppW, text='FOSS ON', width=30, height = 1, font = ('Calibri', 15, "bold"),  command = lambda: ppd('foss','on'), bg = "#44BB55", fg = "white")
	fossOnB.grid(row = 1, column = 2, sticky = "W", padx = 10, pady = 10)

	fossOffB = Button(ppW, text='FOSS OFF', width=30, height = 1, font = ('Calibri', 15, "bold"),  command = lambda: ppd('foss','off'), bg = "#DD8888", fg = "white")
	fossOffB.grid(row = 2, column = 2, sticky = "W", padx = 10, pady = 10)

	fosssB = Button(ppW, text='FOSS STATUS', width=30, height = 1, font = ('Calibri', 15, "bold"),  command = lambda: status('foss'), bg = "#1199FF", fg = "white")
	fosssB.grid(row = 3, column = 2, sticky = "W", padx = 10, pady = 10)

	ltmOnB = Button(ppW, text='LTM ON', width=30, height = 1, font = ('Calibri', 15, "bold"),  command = lambda: ppd('Ltm','On'), bg = "#44BB55", fg = "white")
	ltmOnB.grid(row = 1, column = 3, sticky = "W", padx = 10, pady = 10)

	ltmOffB = Button(ppW, text='LTM OFF', width=30, height = 1, font = ('Calibri', 15, "bold"),  command = lambda: ppd('Ltm','Off'), bg = "#DD8888", fg = "white")
	ltmOffB.grid(row = 2, column = 3, sticky = "W", padx = 10, pady = 10)

	ltmsB = Button(ppW, text='LTM STATUS', width=30, height = 1, font = ('Calibri', 15, "bold"),  command = lambda: status('Ltm'), bg = "#1199FF", fg = "white")
	ltmsB.grid(row = 3, column = 3, sticky = "W", padx = 10, pady = 10)

	alsB = Button(ppW, text='CHANGE ALS', width=30, height = 1, font = ('Calibri', 15, "bold"),  command = als, bg = "#44BB55", fg = "white")
	alsB.grid(row = 4, column = 2, sticky = "W", padx = 10, pady = 10)

	consoleT = Label(ppW, text="", font = ('Calibri', 14), justify = 'left')
	consoleT.grid(row = 6, column = 0, columnspan = 9, sticky = "W", padx = 10, pady = 10)








'''
MAIN Loop
'''


top = Tk()
top.title("ADB")
w, h = top.winfo_screenwidth(), top.winfo_screenheight()
top.geometry("%dx%d+0+0" % (w, h))
# top.geometry("1300x700")

initB = Button(top, text="ROOT,RESUME,SET TIMEOUT",width=30, height = 1, font = ('Calibri', 15, "bold"), command = Tinit, bg = "#44BB55", fg = "white")
initB.grid(row = 0, column = 1, sticky = "W", padx = 10, pady = 10)
initT = Label(top, text="", font = ('Calibri', 14), justify = 'left')
initT.grid(row = 0, column = 2, sticky = "W", padx = 10, pady = 10)

devicesB = Button(top, text="ADB COMMANDS",width=30, height = 1, font = ('Calibri', 15, "bold"), command = devicesWindow, bg = "#1199FF", fg = "white")
devicesB.grid(row = 2, column = 0, sticky = "W", padx = 10, pady = 10)

devicesB = Button(top, text="KEYEVENT COMMANDS",width=30, height = 1, font = ('Calibri', 15, "bold"), command = keyWindow, bg = "#1199FF", fg = "white")
devicesB.grid(row = 3, column = 0, sticky = "W", padx = 10, pady = 10)

shellB = Button(top, text="SHELL STOP/START",width=30, height = 1, font = ('Calibri', 15, "bold"), command = shellWindow, bg = "#1199FF", fg = "white")
shellB.grid(row = 4, column = 0, sticky = "W", padx = 10, pady = 10)

clrsdB = Button(top, text='FREE UP SDCARD', width=30, height = 1, font = ('Calibri', 15, "bold"), command = clearSdcard, bg = "#333333", fg = "white")
clrsdB.grid(row = 5, column = 0, sticky = "W", padx = 10, pady = 10)

buildB = Button(top, text='GET AVAILABLE BUILDS', width=30, height = 1, font = ('Calibri', 15, "bold"), command = buildWindow, bg = "#666666", fg = "white")
buildB.grid(row = 6, column = 0, sticky = "W", padx = 10, pady = 10)

exitB = Button(top, text='EXIT', width=30, height = 1, font = ('Calibri', 15, "bold"), command = exit, bg = "#EE1111", fg = "white")
exitB.grid(row = 0, column = 0, sticky = "W", padx = 10, pady = 10)

dumpsysB = Button(top, text="DUMPSYS",width=30, height = 1, font = ('Calibri', 15, "bold"), command = dumpsysWindow, bg = "#1144FF", fg = "white")
dumpsysB.grid(row = 2, column = 1, sticky = "W", padx = 10, pady = 10)

logB = Button(top, text="LOGGING",width=30, height = 1, font = ('Calibri', 15, "bold"), command = loggingWindow, bg = "#1144FF", fg = "white")
logB.grid(row = 3, column = 1, sticky = "W", padx = 10, pady = 10)

clkB = Button(top, text="CLOCKS",width=30, height = 1, font = ('Calibri', 15, "bold"), command = clocks, bg = "#1144FF", fg = "white")
clkB.grid(row = 4, column = 1, sticky = "W", padx = 10, pady = 10)

panelB = Button(top, text="PANEL ON DUT",width=30, height = 1, font = ('Calibri', 15, "bold"), command = panelDetails, bg = "#44BB55", fg = "white")
panelB.grid(row = 5, column = 1, sticky = "W", padx = 10, pady = 10)

buildB = Button(top, text="BUILD ON DUT",width=30, height = 1, font = ('Calibri', 15, "bold"), command = buildDetails, bg = "#44BB55", fg = "white")
buildB.grid(row = 6, column = 1, sticky = "W", padx = 10, pady = 10)


launchAppB = Button(top, text="APP LAUNCH",width=30, height = 1, font = ('Calibri', 15, "bold"), command = launchAppWindow, bg = "#1199FF", fg = "white")
launchAppB.grid(row = 2, column = 2, sticky = "W", padx = 10, pady = 10)

videoB = Button(top, text="VIDEO PLAYBACK",width=30, height = 1, font = ('Calibri', 15, "bold"), command = videoPlayback, bg = "#1199FF", fg = "white")
videoB.grid(row = 3, column = 2, sticky = "W", padx = 10, pady = 10)

rotB = Button(top, text="ROTATION",width=30, height = 1, font = ('Calibri', 15, "bold"), command = rotateWindow, bg = "#1199FF", fg = "white")
rotB.grid(row = 4, column = 2, sticky = "W", padx = 10, pady = 10)

esdB = Button(top, text="TRIGGER ESD",width=30, height = 1, font = ('Calibri', 15, "bold"), command = esdTrigger, bg = "#DD8888", fg = "white")
esdB.grid(row = 5, column = 2, sticky = "W", padx = 10, pady = 10)

ppB = Button(top, text="POST PROCESSING",width=30, height = 1, font = ('Calibri', 15, "bold"), command = ppWindow, bg = "#DDEECC", fg = "black")
ppB.grid(row = 6, column = 2, sticky = "W", padx = 10, pady = 10)

top.mainloop()
