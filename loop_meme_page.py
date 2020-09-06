import os
import time
import random

import requests

import keyboard
from pynput.keyboard import Key
from pynput.keyboard import Controller as kbController
from pynput.mouse import Button, Controller
import mouse as mouse_get

from selenium import webdriver
from selenium.webdriver.common.by 	import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support 	import expected_conditions
from selenium.webdriver.support.ui 	import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# FUNCTIONS
# 	Login
def login(driver, username, password):
	enter_username = WebDriverWait(driver, 20).until(expected_conditions.presence_of_element_located((By.NAME, 'username')))
	enter_username.send_keys(username)
	enter_password = WebDriverWait(driver, 20).until(expected_conditions.presence_of_element_located((By.NAME, 'password')))
	enter_password.send_keys(password)

	time.sleep(0.5)

	#Click LogIn
	driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]').click()
	time.sleep(5)

	#Remove Notigications		  /html/body/div[4]/div/div/div/div[3]/button[2]
	#driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div/div/button').click()
	driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]').click()
	time.sleep(2)

# Click Inputs
def db_click_sys(coor, button, times):
	mouse.position = coor
	mouse.press(button)
	mouse.press(button)
	mouse.release(button)
	mouse.release(button)
	time.sleep(times)

def click_sys(coor, button, times):
	mouse.position = coor
	mouse.press(button)
	mouse.release(button)
	time.sleep(times)

def write_sys(string,times):
	time.sleep(0.5)
	for c in string:
		keyboard.press(c)
		time.sleep(0.02)
	time.sleep(times)

# Post Functionts
# CLICK POST ON NAVBAR
def post_media():
	global index_post, media_path

	driver.switch_to.window(driver.window_handles[0])
	driver.get('https://www.instagram.com/' + username)
	for x in range(5): print('POSTIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIING'); time.sleep(2); click_sys((1, 1), Button.left, 0.5)
	time.sleep(20)

	click_sys((256, 802), Button.left, 1.5)

	#WRITE MEDIANAME
	click_sys((719, 59), Button.left, 0.5)
	write_sys( media_path , 1 ); 
	keyboard.press(Key.enter); keyboard.release(Key.enter)

	click_sys((232, 549), Button.left, 0.5)
	write_sys( str(index_post), 1 )

	# CLICK ACCEPT FOLDER
	click_sys((898, 576), Button.left, 0.5)

	# CLICK IN-ZOOM
	click_sys((88, 618), Button.left, 0.5)

	# CLICK NEXT BUTTON
	click_sys((411, 224), Button.left, 1)

	# CLICK DESCRIPTION INPUT
	click_sys((138, 279), Button.left, 1)

	# #WRITE DESCRIPTION
	c_desc = clean_description(comments_list[index_post])
	write_sys( c_desc , 1 )

	# CLICK POST BUTTON
	click_sys((433, 225), Button.left, 5)

	click_sys((263, 676), Button.left, 1)


# Unfollow and Follow PEOPLE
ammount_follow, ammount_unf = 0, 0
follow_bool = True

def unFollow_people(follow_bool, hours):
	
	global ammount_follow, ammount_unf


	if follow_bool: driver.switch_to.window(driver.window_handles[2]);
	else:			driver.switch_to.window(driver.window_handles[1]);

	time.sleep(10)

	if hours == 14:
		print('PLEASE SCROLL DOWN')

		time.sleep(100)

	for x in range( 40 ):

		# Get follow Button
		if follow_bool:
			try:		cFollowButton = driver.find_element_by_xpath('/html/body/div[4]/div/div/div[2]/ul/div/li['+str(ammount_follow+1)+']/div/div[3]/button')
			except:
				try:	cFollowButton = driver.find_element_by_xpath('/html/body/div[4]/div/div/div[2]/ul/div/li['+str(ammount_follow+1)+']/div/div[2]/button')
				except:	print('Failed!')
		else:
			try:		cFollowButton = driver.find_element_by_xpath('/html/body/div[4]/div/div/div[2]/ul/div/li['+ str(ammount_unf+300) +']/div/div[3]/button')
			except:	
				try:	cFollowButton = driver.find_element_by_xpath('/html/body/div[4]/div/div/div[2]/ul/div/li['+ str(ammount_unf+300) +']/div/div[2]/button')
				except:	print('Failed!')			

		# Prove if is not already followed
		try:
			if cFollowButton.get_attribute('innerHTML') == 'Follow' or not follow_bool:	
				cFollowButton.click()

				if not follow_bool:
					time.sleep(1)
					try:	driver.find_element_by_xpath('/html/body/div[5]/div/div/div/div[3]/button[1]').click()
					except:	print('failed')

			if x % 10 == 0:		print('Long Sleep', x); 	time.sleep(120)
			else:				print('Sleep', 		x);		time.sleep(10)

			if follow_bool:	ammount_follow	+= 1
			else:			ammount_unf		+= 1
		except:
			try:	driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a').click()
			except:	print('Failed')
			

def clean_description(current_comment):
	current_comment = current_comment.replace('<br>', '\n')

	start_tag_bool = False
	index_loop, first_tag_index = 0, 0
	list_tags_indexs = []

	# GET TAGS INDEX POSITIONS
	for c in current_comment:
		if c == '<': 	start_tag_bool = True;	first_tag_index = index_loop
		if start_tag_bool:
			if c == '>':
				list_tags_indexs.append((first_tag_index, index_loop))
				start_tag_bool = False
		index_loop+=1

	# REMOVE TAGS
	list_tags_indexs = list_tags_indexs[::-1]
	for x in list_tags_indexs:
		c_replace = current_comment[ x[0] : x[1]+1 ]
		current_comment = current_comment.replace( c_replace , '' )

	current_comment += '\n\n #meme #memes #bestmemes #instamemes #funny #funnymemes #dankmemes #offensivememes #edgymemes #spicymemes #nichememes #memepage'

	return current_comment


def prepare_stuff(username):
	
	print('SET AT MOBILE DEVICE')
	driver.get('https://www.instagram.com/' + username)
	time.sleep(20)

	print('Opening 2º Tab and Folowins')
	click_sys((805, 32), Button.left, 1)
	keyboard.press(Key.ctrl); keyboard.press('t'); keyboard.release('t'); keyboard.release(Key.ctrl)
	time.sleep(1)
	driver.switch_to.window(driver.window_handles[1])
	driver.get('https://www.instagram.com/' + username)
	time.sleep(2)
	WebDriverWait(driver, 20).until(expected_conditions.presence_of_element_located((By.XPATH, '/html/body/div[1]/section/main/div/header/section/ul/li[3]/a'))).click()
	time.sleep(2)
	

	print('Opening 3º Tab and Followers')
	click_sys((805, 32), Button.left, 1)
	keyboard.press(Key.ctrl); keyboard.press('t'); keyboard.release('t'); keyboard.release(Key.ctrl)
	time.sleep(1)
	driver.switch_to.window(driver.window_handles[2])
	driver.get('https://www.instagram.com/'+list_p[1])
	time.sleep(2)
	WebDriverWait(driver, 20).until(expected_conditions.presence_of_element_located((By.XPATH, '/html/body/div[1]/section/main/div/header/section/ul/li[2]/a'))).click()
	time.sleep(2)
	


# Driver OF ChromeBot
driver 		= webdriver.Chrome(ChromeDriverManager().install())

# Fake Inputs of Keyboard and Mouse
keyboard 	= kbController()
mouse 		= Controller()

# Get Time
start_milliseconds = time.time()
start_milliseconds -= 4000

# Loop Engine
loop = True
index_action = 0
hours_passed = 0

index_post = 1
index_loop = 0

# Data
list_p = ['lanarhoades', 'dangershewrote', 'titsoutkickedout', 'mia_malkova', 'brandi_love', 'realnicoleaniston']

username, password = 'coronao_gang', 'Contra06.' #vladimir_ilych_lenin_

media_path = 'C:/Users/Acolm/Desktop/Canon/media'

comments = open("descriptions.txt","r")
comments_list = []

# Get Description Array
line = comments.readline()
while line:
    comments_list.append(line)
    line = comments.readline()



# LOGIN AND START
driver.get('https://www.instagram.com')
login(driver, username, password)

prepare_stuff(username)

while loop:

	if time.time() - start_milliseconds >= 1800:
		index_loop+=1

		start_milliseconds = time.time()
		
		post_media()

		if hours_passed % 1 == 0:
			unFollow_people(follow_bool, hours_passed)

			follow_bool = not follow_bool if hours_passed >= 14 else True

		index_post += 1
		hours_passed += 0.5

		print(hours_passed, index_post, index_loop)

	time.sleep(5)



print('Finished')















# 53100000
# 15991373





































