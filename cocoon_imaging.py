from picamera2 import Picamera2, Preview
import time
import sys
import os
import re

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
	
print(im_out_list)
print(im_num)


def img_capture():
	global im_num
	
	
	cam.start_preview(Preview.QTGL)
	cam.start()
	while True:
		im_num += 1
		input('Press any key to capture')
		
		filename = f'img{str(im_num).zfill(3)}.jpg'
		cam.capture_file('./output/' + filename)
		print(f'\nCaptured {filename}')
		
		input_choice = input('\n   Press "n" to take another image, press "q" to return to the main menu.\n\n')
		if input_choice == 'q':
			cam.stop_preview()
			cam.stop()
			break
		else:
			continue
		
		

def main():
	while True:
		print('\n\nWelcome to the Mason Bee Imaging Adventure.\n\nWould you like to:\n   1. Continue where you left off\n   2. Retake a particular image\n   3. Give up for now\n   4. There are no more cocoons to image\n\n')

		input_num = input('Enter your choice: ')

		if input_num == '1':
			if im_num == 0:
				print('\n\nYour great journey begins.\n\n')
			else:
				print('\n\nWelcome back. We missed you.\n\n')
			img_capture()
		elif input_num == '2':
			print('\nThis feature has not been built yet. Shame my creator')
		elif input_num == '3':
			print('\nThere is no escape')
			break
		elif input_num == '4':
			print('\nI am so proud of you. You are released from your burden.')
			break
		else:
			print('\nTry again')


if __name__ == '__main__':
	main()
