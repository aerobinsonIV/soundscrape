import os

from mutagen.easyid3 import EasyID3

def clean(input_name):
	if "[Explicit]" in input_name:
		return input_name[:input_name.find("[Explicit]") - 1]
	else:
		return input_name

dir_list = os.listdir()

for file in dir_list:
	if ".mp3" in file:
		print("doing " + file)
		audio = EasyID3(file) #open file
		
		audio['title'] = u"" + clean(audio['title'][0])
		audio['album'] = u"" + clean(audio['album'][0])

		audio.save()
