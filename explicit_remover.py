import os
from mutagen.easyid3 import *

# TODO: This whole script needs work
def clean_filename(input_name):
	if "[Explicit]" in input_name:
		return input_name[input_name.find(" - ") + 3:input_name.find("[Explicit]") - 1]
	else:
		return input_name[input_name.find(" - ") + 3:input_name.find(".mp3")]	

def clean(input_name):
	if "[Explicit]" in input_name:
		return input_name[:input_name.find("[Explicit]") - 1]
	else:
		return input_name

if __name__ == "__main__":
	dir_list = os.listdir(os.path.join(os.getcwd(), "temp"))
	for file in dir_list:
		if ".mp3" in file:
			print("doing " + file)
			audio = EasyID3(os.path.join(os.getcwd(), "temp", file)) #open file
			
			audio['title'] = u"" + clean(audio['title'][0])
			audio['album'] = u"" + clean(audio['album'][0])

			audio.save()
			os.rename(os.path.join(os.getcwd(), "temp", file), os.path.join(os.getcwd(), "temp", clean(file)+ ".mp3"))
