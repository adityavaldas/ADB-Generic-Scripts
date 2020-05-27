#!python3
import os
import subprocess
os.system('adb wait-for-device root')
def composition_result():
	dumpsys=subprocess.getoutput(["adb","shell","dumpsys","SurfaceFlinger"])
	dump_list=dumpsys.split("\n")
	for line_no in range(len(dump_list)):
		if dump_list[line_no].find("Idx")>-1:
			first_line=line_no
		if "Allocated buffers" in dump_list[line_no]:
			last_line=line_no
	display_comp_list=dump_list[first_line:last_line]
	for line in display_comp_list:
		print(line)
while 1:
	composition_result()
	a=input("Press Enter to continue or Q to exit:")
	if(a.lower()=="q"):
		exit()
