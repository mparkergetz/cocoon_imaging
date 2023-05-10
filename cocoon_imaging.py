from picamera2 import Picamera2, Preview
import time
import sys
import os
import re
import json


cam = Picamera2()
cam_config = cam.create_still_configuration(main = {'size': (1920, 1080)}, lores = {'size': (640, 480)}, display = 'lores')
cam.configure(cam_config)

im_out_list = os.listdir('./output/')
im_out_list.sort()
 
if im_out_list == []:
	im_num = 0
else:
	last_im = im_out_list[-1]
	im_num = int(re.search('\d+', im_out_list[-1])[0])
	
def dict_check():
	home_files = os.listdir('./')
	if 'label_table.json' in home_files:
		with open('label_table.json', 'r') as file:
			label_dict = json.load(file)
	else:
		label_dict = {}
	return label_dict
	


def img_capture(im_num, label_dict):
	cam.start_preview(Preview.QTGL)
	cam.start()
	while True:
		im_num += 1
		input('Press any key to capture')
		
		filename = f'img{str(im_num).zfill(3)}.jpg'
		cam.capture_file('./output/' + filename)
		print(f'\nCaptured {filename}')
		
		label = input('Label: ')
		
		label_dict[filename] = label
		
		#print(f'\n\nImage: {filename}\nLabel: {label}\n\n')
		
		confirm = input('Confirm image/label info is good (y/n)  ')
		if confirm == 'n':
			label = input(f'\n\nImage: {filename}\nLabel: ')
			label_dict[filename] = label		
		
		input_choice = input('\n   Press "n" to take another image, press "q" to save and return to the main menu.\n\n')
		if input_choice == 'q':
			with open('label_table.json', 'w') as file:
				json.dump(label_dict, file)
			
			cam.stop_preview()
			cam.stop()
			break
		else:
			continue
		
def write_out_json(label_dict):
	import csv
	fields = ['image', 'label']
	with open('label_table.csv', 'w', newline = '') as file:
		csvwriter = csv.writer(file)
		csvwriter.writerow(fields)
		for image in label_dict:
			label = label_dict[image]
			csvwriter.writerow([image,label])	

def main():
	while True:
		print('\n\nWelcome to the Mason Bee Imaging Adventure.\n\nWould you like to:\n   1. Continue where you left off\n   2. Check your label dictionary\n   3. Exit\n\n   9. There are no more cocoons to image\n\n')

		input_num = input('Enter your choice: ')

		if input_num == '1':
			if im_num == 0:
				print('\n\nYour great journey begins.\n\n')
			else:
				print('\n\nWelcome back. We missed you.\n\n')
				
			label_dict = dict_check()
			print(label_dict)
			
			img_capture(im_num, label_dict)
			
		elif input_num == '2':
			try:
				for entry in label_dict:
					print(f'{entry}: {label_dict[entry]}')
			except:
				print('\n\n*****Dict not in memory yet****\n\n')
		elif input_num == '3':
			print('\nGreat work today')
			break
		elif input_num == '9':
			print('\nI am so proud of you. You are released from your burden.')
			
			write_out_json(label_dict)
			
			break
		else:
			print('\nTry again')


if __name__ == '__main__':
	main()
