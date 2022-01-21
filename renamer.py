import os

def clean_filename(input_name):
	if "[Explicit]" in input_name:
		return input_name[input_name.find(" - ") + 3:input_name.find("[Explicit]") - 1]
	else:
		return input_name[input_name.find(" - ") + 3:input_name.find(".mp3")]	

dir_list = os.listdir()

for file in dir_list:
	if ".mp3" in file:
		os.rename(file, clean_filename(file) + ".mp3")