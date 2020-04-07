
import os
import time
import sys
import json

video_index = 1
filename = 'videos.json'

def sprint(string, tm=1):
	print(string)


def html_page_handle_and_download(file_name, name):
	print("\033[1;32;40m")
	global video_index
	with open(file_name, "r") as file:
		i = 1
		for con in file:
			# ERROR
			if i== 1 and con == '{"error":true,"iframe":true}':
				video_url = con
			if i == 63:
				video_url = con
				break
			i+=1
		if video_url == '{"error":true,"iframe":true}':
			sprint("\033[1;31;40mYour video id is not valid\033[0;37;40m", 2)
		else:
#			print(video_url)
			new_video_url = video_url.split("url")[1].split(',')[0].split('"')[2]
			os.system("curl -O {}".format(new_video_url))
			video_name = video_url.split("url")[1].split(',')[0].split('"')[2].split("/")[4]
			video_name_and_index = name # "Video " + str(video_index) + ".mp4"
			video_index += 1
			os.rename(video_name, video_name_and_index)
		os.system("rm -rf {}".format(file_name))
	print("\033[0;37;40m")


def download_folder():
	try:
		username = os.path.expanduser("~").split('/')[2]
		sprint("\033[1;32;40mPlease enter the PATH of download folder: \033[0;37;40m", 2)
		sprint("\033[1;31;40m\t\tExample: \033[0;37;40m/Users/{}/Desktop".format(username), 2)
		sprint("\033[1;31;40m\t\tExample: \033[0;37;40m/Volumes/Storage/goinfre/{}".format(username), 2)

		folder_path = input("PATH: \033[1;33;40m")
		print("\033[0;37;40m")
		folder_path += "/wistia-downloader/"
		os.system("mkdir {} 2>/dev/null".format(folder_path))
		os.system("cp {} {} 2>/dev/null".format(filename, folder_path))
		os.chdir("{}".format(folder_path))
#		sprint("\033[1;33;40mOpening the download folder...\033[0;37;40m", 2)
#		os.system("open {}".format(folder_path))
	except FileNotFoundError:
		print("\033[1;31;40mThe PATH does not exist !! try again\033[0;37;40m")
		sprint(".....", 100)
		main()


def main():
	os.system("clear")
	download_folder()
	url = "https://fast.wistia.net/embed/iframe/"
	i = 0
	with open(filename, "r+") as video_id:
		if os.stat(filename).st_size == 0:
			print("")
			sprint("\033[1;31;40mThe file is empty !!\033[0;37;40m", 0.2)
			sprint(".....", 100)
			main()
		ids = json.load(video_id)
		for record in ids:
			if 'disabled' in record:
				continue 
			id = record['embedUrl'].rsplit('/', 1)[-1]
			name = record['name'] # .split('IEC',1)[1]
#			print('id:' + id + ', name: ' + name)

			os.system("curl -O {}".format(url + id))
			print("Video ID " + str(i + 1) + ' ' + name + " -------------------------------------------------")
			html_page_handle_and_download(id.rstrip(), name)
			print("-----------------------------------------------------------------------------------")
			i+=1 

	

if __name__ == '__main__':
	main()
