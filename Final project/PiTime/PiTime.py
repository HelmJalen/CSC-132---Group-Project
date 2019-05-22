# -*- coding: utf-8 -*-
########################################################################################################################################################
##Names: Broady Rivet, Quran Coleman, Mariela A., Jaylen H., Jordan B.                                                                                ##
##Description: This code pulls questions off a online thread and sets a random 10 into a random order. also pulls sounds and background images from   ##
##              folder the program is found in.                                                                                                       ##
########################################################################################################################################################

############################
##IMPORTANT NOTICE!!!!!!!!##
############################


##Run program with python 3 (any version)
##To run put all files into a folder at the location: "/home/pi/PiTime"


import pygame
import sys
## Constants in pygame
from pygame.locals import *
import RPi.GPIO as GPIO
## Request library to get the thread's questions
import urllib.request
from datetime import datetime
## Library to store an exchange any type of data
import json
from random import randint
##used for various fonts
from pprint import pprint
import time
## Used for serializing and deserializing object structures
import pickle
import collections
## Allows use of Pi dependent functionality
import os
from operator import itemgetter, attrgetter, methodcaller

## Game variables
PlayIt = True
Cont = True
TimeStamp = time.time()
PressedButton = -1
strName = ''

## Sounds used in game
Start_Sound = "/home/pi/PiTime/start.mp3"
Correct_Sound = "/home/pi/PiTime/correct.mp3"
Incorrect_Sound = "/home/pi/PiTime/incorrect.mp3"
Score_Sound = "/home/pi/PiTime/score.mp3"
Beep_Sound = "/home/pi/PiTime/beep.mp3"

## Each phase of the game is listed below as f_PHASE NAME
f_START = 0
f_MENU = 1
f_ID = 2
f_QUESTIONS = 3
f_RESULTS = 4
f_TOP = 5

present_phase = f_START

## Every color used being initialized
cWHITE   = (255, 255, 255)
cBLACK    = (0, 0, 0)
cRED     = (255, 0, 0)
cBLUE     = (0, 0, 255)

## Buttons pin setup
red = 16
yellow = 12
green = 26
blue =  23

## GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(red, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(yellow, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(green, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(blue, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Define the buttons
def Push(channel):
	global TimeStamp
	global PressedButton
	time_now = time.time()
	if (time_now - TimeStamp >= 0.3):
		PressedButton = channel
	TimeStamp = time_now

## Buttons' push detection

GPIO.add_event_detect(red, GPIO.BOTH, callback=Push)
GPIO.add_event_detect(yellow, GPIO.BOTH, callback=Push)
GPIO.add_event_detect(green, GPIO.BOTH, callback=Push)
GPIO.add_event_detect(blue, GPIO.BOTH, callback=Push)

## Actual game initialization
pygame.init()
## Music Initialization
pygame.mixer.init()

## Initialize the fonts used

myfont = pygame.font.SysFont("monospace", 15)

## Hide the mouse while game is on
pygame.mouse.set_visible(False)

#Width and length of screen
Dimensions = [480,320]
## Makes game take entire screen of pi
Screen = pygame.display.set_mode(Dimensions, pygame.FULLSCREEN)
InitialPosition = [0,0]

## How fast screen refresh
Clock = pygame.time.Clock()

## Formatting functions for pulled questions
def Question_Generator_Adddition1():
	arg1 = randint(0, 9)
	arg2 = randint(0, 9)
	arg3 = randint(1, 2)
	question = r'{"category": "1st Grade", "type": "multiple", "difficulty": "easy", "question": "¿What is the summation of ' + str(arg1) + ' plus ' + str(arg2) +'?", "correct_answer": "' + str(arg1+arg2) + r'", "incorrect_answers": ["' + str(arg1+arg2+arg3) + r'", "' + str(arg1+arg2-arg3) + r'", "' + str(arg1+arg2+arg3+1) + r'"]}'
	return question;

def Question_Generator_Addition2():
	arg1 = randint(0, 80)
	arg2 = randint(0, 99)
	arg3 = randint(1, 20)
	question = r'{"category": "1st Grade", "type": "multiple", "difficulty": "easy", "question": "¿What is the summation of ' + str(arg1) + ' plus ' + str(arg2) +'?", "correct_answer": "' + str(arg1+arg2) + r'", "incorrect_answers": ["' + str(arg1+arg2+arg3) + r'", "' + str(arg1+arg2-arg3) + r'", "' + str(arg1+arg2+arg3+1) + r'"]}'
	return question;

def Question_Generator_Addition_Easy():
	arg1u = randint(0, 9)
	arg1d = randint(0, 9)
	arg2u = randint(0, 9)
	arg2d = randint(0, 9)
	arg3 = randint(1, 20)
	while (arg2u+arg1u>9):
		arg2u = randint(0, 9)
	while (arg2d+arg1d>9):
		arg2d = randint(0, 9)
	arg1 = arg1d*10 + arg1u
	arg2 = arg2d*10 + arg2u
	question = r'{"category": "1st Grade", "type": "multiple", "difficulty": "easy", "question": "¿What is the summation of ' + str(arg1) + ' plus ' + str(arg2) +'?", "correct_answer": "' + str(arg1+arg2) + r'", "incorrect_answers": ["' + str(arg1+arg2+arg3) + r'", "' + str(arg1+arg2-arg3) + r'", "' + str(arg1+arg2+arg3+1) + r'"]}'
	return question;

def Question_Generator_Greater_Than():
	arg1 = randint(0, 95)
	good = arg1 + randint(1,100-arg1)
	bad1 = arg1 - randint(0, arg1)
	bad2 = arg1 - randint(0, arg1)
	bad3 = arg1 - randint(0, arg1)
	question = r'{"category": "1st Grade", "type": "multiple", "difficulty": "easy", "question": "¿Which of these numbers is greater than ' + str(arg1) +'?", "correct_answer": "' + str(good) + r'", "incorrect_answers": ["' + str(bad1) + r'", "' + str(bad2) + r'", "' + str(bad3) + r'"]}'
	return question;

def Question_Generator_Less_Than():
	arg1 = randint(0, 95)
	good = arg1 - randint(1,arg1)
	bad1 = arg1 + randint(0, 100-arg1)
	bad2 = arg1 + randint(0, 100-arg1)
	bad3 = arg1 + randint(0, 100-arg1)
	question = r'{"category": "1st Grade", "type": "multiple", "difficulty": "easy", "question": "¿Which of these numbers is less than' + str(arg1) +'?", "correct_answer": "' + str(good) + r'", "incorrect_answers": ["' + str(bad1) + r'", "' + str(bad2) + r'", "' + str(bad3) + r'"]}'
	return question;

def Question_Generator_Series():
	Good = []
	Good.append(randint(0, 99))
	val = randint(0, 99)
	while (val in Good):
		val = randint(0, 99)
	Good.append(val)
	val = randint(0, 99)
	while (val in Good):
		val = randint(0, 99)
	Good.append(val)
	Good.sort()
	strGood = str(Good[0]) + ' < ' + str(Good[1]) + ' < '  + str(Good[2])

	Bads = []
	iBads = 0
	while (iBads<3):
		Bad = []
		Bad.append(randint(0, 99))
		val = randint(0, Bad[0])
		while (val in Bad):
			val = randint(0, Bad[0])
		Bad.append(val)
		val = randint(Bad[1], 99)
		while (val in Bad):
			val = randint(Bad[1], 99)
		Bad.append(val)
		strBad = str(Bad[0]) + ' < ' + str(Bad[1]) + ' < '  + str(Bad[2])
		Bads.append(strBad)
		iBads = iBads + 1

	question = r'{"category": "1st Grade", "type": "multiple", "difficulty": "easy", "question": "Which of these is the correct series?", "correct_answer": "' + strGood + r'", "incorrect_answers": ["' + Bads[0] + r'", "' + Bads[1] + r'", "' + Bads[2] + r'"]}'
	return question;

def Question_Generator_BeforeA():
arg1 = randint(5, 99)
	good = arg1 - 1
	bad1 = arg1 - randint(1, 10)
	bad2 = arg1 - randint(1, 10)
	while (bad2 == bad1):
		bad2 = arg1 - randint(1, 10)
	bad3 = arg1 - randint(1, 10)
	while ((bad3 == bad1) or (bad3 == bad2)):
		bad3 = arg1 - randint(1, 10)
	question = r'{"category": "1st Grade", "type": "multiple", "difficulty": "easy", "question": "¿Which of these numbers goes before ' + str(arg1) +'?", "correct_answer": "' + str(good) + r'", "incorrect_answers": ["' + str(bad1) + r'", "' + str(bad2) + r'", "' + str(bad3) + r'"]}'
	return question;

## If elementry level question is grabbed replace it
def Question_Generator_Elementary():
	questions = r'{"response_code": 0,"results": ['
	qt = 0
	while (qt<10):
		category = randint(0,5)
		if (category == 0):
			questions = questions + Question_Generator_Adddition1()
		if (category == 1):
			questions = questions + Question_Generator_Addition_Easy()
		if (category == 2):
			questions = questions + Question_Generator_Greater_Than()
		if (category == 3):
			questions = questions + Question_Generator_Less_Than()
		if (category == 4):
			questions = questions + gQuestion_Generator_Serie()
		if (category == 5):
			questions = questions + Question_Generator_BeforeA()
		qt = qt + 1
		if (qt < 10):
			questions = questions + ','
	questions = questions + ']}'
	return questions

## Function to create letters for name wheel
def ABC (pos):
print("inside ABC. Pos=("+str(pos[0])+","+str(pos[1])+")")
	letter = ''
	if 24 <= pos[0] <= 57 and 117 <= pos[1] <= 157:		        # A
		letter = 'A'
	elif 74 <= pos[0] <= 107 and 117 <= pos[1] <= 157:		# B
		letter = 'B'
	elif 124 <= pos[0] <= 157 and 117 <= pos[1] <= 157:		# C
		letter = 'C'
	elif 174 <= pos[0] <= 207 and 117 <= pos[1] <= 157:		# D
		letter = 'D'
	elif 224 <= pos[0] <= 257 and 117 <= pos[1] <= 157:		# E
		letter = 'E'
	elif 274 <= pos[0] <= 307 and 117 <= pos[1] <= 157:		# F
		letter = 'F'
	elif 324 <= pos[0] <= 357 and 117 <= pos[1] <= 157:		# G
		letter = 'G'
	elif 374 <= pos[0] <= 407 and 117 <= pos[1] <= 157:		# H
		letter = 'H'
	elif 424 <= pos[0] <= 457 and 117 <= pos[1] <= 157:		# I
		letter = 'I'
	elif 24 <= pos[0] <= 57 and 167 <= pos[1] <= 207:		# J
		letter = 'J'
	elif 74 <= pos[0] <= 107 and 167 <= pos[1] <= 207:		# K
		letter = 'K'
	elif 124 <= pos[0] <= 157 and 167 <= pos[1] <= 207:		# L
		letter = 'L'
	elif 174 <= pos[0] <= 207 and 167 <= pos[1] <= 207:		# M
		letter = 'M'
	elif 224 <= pos[0] <= 257 and 167 <= pos[1] <= 207:		# N
		letter = 'N'
	elif 324 <= pos[0] <= 357 and 167 <= pos[1] <= 207:		# O
		letter = 'O'
	elif 374 <= pos[0] <= 407 and 167 <= pos[1] <= 207:		# P
		letter = 'P'
	elif 424 <= pos[0] <= 457 and 167 <= pos[1] <= 207:		# Q
		letter = 'Q'
	elif 24 <= pos[0] <= 57 and 217 <= pos[1] <= 257:		# R
		letter = 'R'
	elif 74 <= pos[0] <= 107 and 217 <= pos[1] <= 257:		# S
		letter = 'S'
	elif 124 <= pos[0] <= 157 and 217 <= pos[1] <= 257:		# T
		letter = 'T'
	elif 174 <= pos[0] <= 207 and 217 <= pos[1] <= 257:		# U
		letter = 'U'
	elif 224 <= pos[0] <= 257 and 217 <= pos[1] <= 257:		# V
		letter = 'V'
	elif 274 <= pos[0] <= 307 and 217 <= pos[1] <= 257:		# W
		letter = 'W‘'
	elif 324 <= pos[0] <= 357 and 217 <= pos[1] <= 257:		# X
		letter = 'X'
	elif 374 <= pos[0] <= 407 and 217 <= pos[1] <= 257:		# Y
		letter = 'Y'
	elif 424 <= pos[0] <= 457 and 217 <= pos[1] <= 257:		# Z
		letter = 'Z'

	print("letter="+letter)
	return letter

## Set game to True to play
while (PlayIt == True):
	# -------- Initial Screen -----------
	if ((PlayIt == True) and (present_phase == f_START)):
		## Restarts the screen and sets the color for the background
		screen.fill(cWHITE)

	## Shows actual png image for screen
	image = pygame.image.load("/home/pi/PiTime/StartScreen.png").convert()
	screen.blit(image, InitialPosition)

	## Timer for screen
	Clock.tick(20)

	## Refresh the screen
	pygame.display.flip()

	pygame.mixer.music.load(Start_Sound)
	pygame.mixer.music.play(0)

	## Wait for button
	PressedButton = -1
	Cont = True
	while (Cont):
		## Yellow button quits game
		if (PressedButton == yellow):
			PressedButton = -1
			PlayIt = False
			Cont = False
		## Red button brings up menu
		if (PressedButton == red):
			PressedButton = -1
			Cont = False
			present_phase == f_MENU

	# -------- MENU -----------
	if (PlayIT and (present_phase == f_MENU)):

		screen.fill(cWHITE)

		image = pygame.image.load("/home/pi/PiTime/MenuScreen.png").convert()
		screen.blit(image, InitialPosition)

		Clock.tick(20)

		pygame.display.flip()

		pygame.mixer.music.load(Beep_Sound)
		pygame.mixer.music.play(0)

		PressedButton = -1
		Cont = True
		while (Cont):
			## Red brings to name select
			if (PressedButton == red):
				PressedButton = -1
				present_phase = f_ID
				Cont = False
			## Yellow brings up top 5 scores
			if (PressedButton == yellow):
				PressedButton = -1
				present_phase = f_TOP
				Cont = False
			## Green goes back
			if (PressedButton == green):
				PressedButton = -1
				present_phase = f_START
				Cont = False

	# -------- Top Scores -----------
	if (PlayIt and (present_phase == f_TOP)):

		pantalla.fill(cWHITE)

		image = pygame.image.load("/home/pi/PiTime/Top5.png").convert()
		screen.blit(image, InitialPosition)

		# Get the HighScores
		high_scores = {}
		if (os.path.exists('/home/pi/PiTime/HighScores.txt')) and (os.path.getsize('/home/pi/PiTime/HighScores.txt')>0):
			high_scores = json.load(open('/home/pi/PiTime/HighScores.txt'))
		else:
			high_scores = {}

		## Iteration for the results
		i = 1
		for key, scores in high_scores.items():
			for item in sorted(sorted(sorted(scores, key=itemgetter(3), reverse=False), key=itemgetter(2), reverse=True), key=itemgetter(4), reverse=True):
				name = item[0]
				note = item[1]
				time = item[3]
				percentage = item[4]
				font = pygame.font.SysFont('arial', 22)
				message = fuente.render(str(i), 1, cRED)
				screen.blit(message, (40-message.get_rect().width/2, 52+i*18))
				font = pygame.font.SysFont('arial', 22)
				message = font.render(name, 1, cBLUE)
				screen.blit(message, (60, 52+i*18))
				message = font.render(str(note), 1, cBLUE)
				screen.blit(message, (300-message.get_rect().width/2, 52+i*18))
				message = font.render(str(time), 1, cBLUE)
				screen.blit(message, (380-message.get_rect().width/2, 52+i*18))
				i = i + 1

		Clock.tick(20)

		pygame.display.flip()

		pygame.mixer.music.load(Correct_Sound)
		pygame.mixer.music.play(0)

		PressedButton = -1
		Cont = True
		while (Cont):
			## Red button returns to menu
			if (PressedButton == red):
				PressedButton = -1
				present_phase = f_MENU
				Cont = False

	# -------- ID -----------
	if (PlayIt and (present_phase == f_ID)):

		screen.fill(cWHITE)

		image = pygame.image.load("/home/pi/PiTime/NameSelect.png").convert()     ##### change file name from quiz_pantalla_21_NOMBRE_ingles.png to quiz_screen_name.png
		screen.blit(image, InitialPosition)

		font = pygame.font.SysFont('arial', 64)
		message = font.render('A', 1, cBLUE)
		screen.blit(message, (240-message.get_rect().width/2, 130))

		Clock.tick(20)

		pygame.display.flip()

		pygame.mixer.music.load(Beep_Sound)
		pygame.mixer.music.play(0)

		PressedButton = -1
		Cont = True
		## Bring back all the old letters made earlier
		aLetter = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','<<']
		iLetter = 0
		strName = ''
		while (Cont):

			## Red selects current letter
			if (PressedButton == red):
				PressedButton = -1
				if iLetter == 27:
					strName = strName[:-1]
				else:
					if len(strName)<15:
						strName = strName + aLetter[iLetter]
				# Cleans the screen and sets the color for the background
				screen.fill(cWHITE)
				# Initial screen
				image = pygame.image.load("/home/pi/PiTime/NameSelect.png").convert()
				screen.blit(image, InitialPosition)
				font = pygame.font.SysFont('arial', 24)
				message = font.render(strName, 1, cBLUE)
				screen.blit(message, (240-message.get_rect().width/2, 73))
				font = pygame.font.SysFont('arial', 64)
				message = font.render(aLetter[iLetter], 1, cBLUE)
				screen.blit(message, (240-messafe.get_rect().width/2, 130))
				pygame.display.flip()
				pygame.mixer.music.load(Beep_Sound)
				pygame.mixer.music.play(0)

				#Blue goes to previous letter
			if (PressedButton == blue):
				pressedButton = -1
				iLetter = iLetter - 1
				if iLetter < 0:
				iLetter = 27
				# Cleans the screen and sets the color for the background
				screen.fill(cWHITE)
				image = pygame.image.load("/home/pi/PiTime/NameSelect.png").convert()   ####change file name from quiz_pantalla_21_NOMBRE_ingles.png to quiz_screen_name.png
				screen.blit(image, InitialPosition)
				font = pygame.font.SysFont('arial', 24)
				message = font.render(strName, 1, cBLUE)
				screen.blit(message, (240-message.get_rect().width/2, 73))
				font = pygame.font.SysFont('arial', 64)
				message = font.render(aLetter[iLetter], 1, cBLUE)
				screen.blit(message, (240-message.get_rect().width/2, 130))
				pygame.display.flip()
				pygame.mixer.music.load(Beep_Sound)
				pygame.mixer.music.play(0)

				## Yellow moves onto next color
			if (PressedButton == yellow):
				PressedButton = -1
				iLetter = iLetter + 1
				if iLetter > 27:
				iLetter = 0
				screen.fill(cWHITE)
				image = pygame.image.load("/home/pi/PTime/NameSelect.png").convert()
				screen.blit(image, InitialPosition)
				font = pygame.font.SysFont('arial', 24)
				message = font.render(strName, 1, cBLUE)
				screen.blit(message, (240-message.get_rect().width/2, 73))
				font = pygame.font.SysFont('arial', 64)
				message = font.render(aLetter[iLetter], 1, cBLUE)
				screen.blit(message, (240-message.get_rect().width/2, 130))
				pygame.display.flip()
				pygame.mixer.music.load(Beep_Sound)
				pygame.mixer.music.play(0)

				## Green starts the game
			if (PressedButton == green):
				present_phase = f_QUESTIONS
				Cont = False

	# -------- QUESTIONS -----------
	if (PlayIt and (present_phase == f_QUESTIONS)):
		InitialInst = datetime.now()
		score = 0
		## adds score
		score = int(score)

		NResponse = 10
		nResponse = 0

		#URL
		url = 'https://opentdb.com/api.php?amount=10&category=9&difficulty=easy&type=multiple'
		## Alternate url below
		## url = 'https://opentdb.com/api.php?amount=10&type=multiple'
		req = urllib.request.Request(url)
		r = urllib.request.urlopen(req).read()
		data = json.loads(r.decode('utf-8-sig'))

		while (nResponse < NResponse):

			screen.fill(cWHITE)

			image = pygame.image.load("/home/pi/PiTime/QuestionScreen.png").convert()
			screen.blit(image, InitialPosition)

			## Write the question
			font = pygame.font.SysFont('/home/pi/PiTime/Antonio-Bold.ttf', 36)

			txtQuestion = 'Question ' + str(nResponse+1)
			message = font.render(txtQuestion, 1, cBLUE)
			screen.blit(message, (40, 10))

			font = pygame.font.SysFont('/home/pi/PiTime/Antonio-Light.ttf', 28)
			txtQuestion = data['results'][nResponse]['question'].replace('"','\\"').replace("'","\\'").replace("&shy;",'').replace("&quot;",'"').replace('&#039;',"'")
			if len(txtQuestion)<=45:
				txtLine1 = txtQuestion
				message = font.render(txtQuestion, 1, cBLUE)
				screen.blit(message, (40, 55))
			elif len(txtQuestion)<=90:
				txtLine1 = txtQuestion[:45]
				txtLine2 = txtQuestion[45:]
				message = font.render(txtLine1, 1, cBLUE)
				screen.blit(message, (40, 47))
				message = font.render(txtLine2, 1, cBLUE)
				screen.blit(message, (40, 73))
			else:
				txtLine1 = txtQuestion[:45]
				txtLine2 = txtQuestion[45:]
				txtLine3 = txtLine2[45:]
				txtLine2 = txtLine2[:45]
				message = font.render(txtLine1, 1, cBLUE)
				screen.blit(message, (40, 47))
				message = font.render(txtLine2, 1, cBLUE)
				screen.blit(message, (40, 66))
				message = font.render(txtLine3, 1, cBLUE)
				screen.blit(message, (40, 85))

			randomnumber = randint(0, 3)
			i = 0
			nr = 0;
			response = "";
			while (i < 4):
				if (i == randomnumber):
					txtResponse = data['results'][nResponse]['correct_answer'].replace('"','\\"').replace("'","\\'").replace('&shy;','').replace('&quot;','"').replace('&#039;',"'")
					## Write the answer
					font = pygame.font.SysFont('/home/pi/PiTime/Antonio-Bold.ttf', 28)
					message = font.render(txtResponse, 1, cBLUE)
					screen.blit(message, (142, 129+i*50))
				else:
					txtResponse = data['results'][nResponse]['incorrect_answers'][nr].replace('"','\\"').replace("'","\\'").replace('&shy;','').replace('&quot;','"').replace('&#039;',"'")
					## Write the answer
					font = pygame.font.SysFont('/home/pi/PiTime/Antonio-Bold.ttf', 28)
					message = font.render(txtResponse, 1, cBLUE)
					screen.blit(message, (142, 129+i*50))
					nr = nr + 1
				i = i + 1

			Clock.tick(20)

			pygame.display.flip()

			pygame.mixer.music.load(Beep_Sound)
			pygame.mixer.music.play(0)

			PressedButton = -1
			qResponse = ' '
			Cont = True
			while (Cont):
				## Sets buttons' actions for the questions
				if (PressedButton == red):
					PressedButton = -1
					qResponse = '0'
					Cont = False
				if (PressedButton == blue):
					PressedButton = -1
					qResponse = '1'
					Cont = False
				if (PressedButton == yellow):
					PressedButton = -1
					qResponse = '2'
					Cont = False
				if (PressedButton == green):
					PressedButton = -1
					qResponse = '3'
					Cont = False

				## Refresh the timer
				FinalInst = datetime.now()
				time = FinalInst - InitialInst
				secs = time.seconds
				pygame.draw.rect(screen,cWHITE,(280,0,479,50))
				font = pygame.font.Font('/home/pi/PiTime/Antonio-Regular.ttf', 18)
				txtQuestion = 'Time: ' + str(secs) + ' seconds'
				message = font.render(txtQuestion, 1, cBLACK)
				screen.blit(message, (380-message.get_rect().width/2, 20))

				Clock.tick(20)

				pygame.display.flip()

			if (qResponse != str(randomnumber)):

				screen.fill(cWHITE)

				## Wrong answer screen
				image = pygame.image.load("/home/pi/PiTime/Wrong.png").convert()
				screen.blit(image, InitialPosition)

				Clock.tick(20)

				pygame.display.flip()

				pygame.mixer.music.load(Incorrect_Sound)
				pygame.mixer.music.play(0)

				## Wait 3 seconds
				time.sleep(3)
			else:

				screen.fill(cWHITE)

				## Correct answer screen
				image = pygame.image.load("/home/pi/PiTime/Correct.png").convert()

				screen.blit(image, InitialPosition)

				Clock.tick(20)

				pygame.display.flip()

				pygame.mixer.music.load(Correct_Sound)
				pygame.mixer.music.play(0)

				time.sleep(3)
				score = score + 1

			FinalInst = datetime.now()
			time = FinalInst - InitialInst
			secs = time.seconds

			## Results
			nResponse = nResponse + 1

		FinalInst = datetime.now()
		time = FinalInst - InitialInst
		secs = time.seconds
		minutes=int(secs/60)
		Secs=secs-minutes*60

		# Final results
		#print ('Your final results are: ' + str(score) + ' correct ' + str(NResponse) + ' in ' + str(minutes) + ':' + str(Secs) + '.\n')

		# Erase the screen
		screen.fill(cWHITE)

		# Shows the question background
		image = pygame.image.load("/home/pi/PiTime/EndResult.png").convert()
		screen.blit(image, InitialPosition)

		#Write the text
		font = pygame.font.SysFont('arial', 32)
		txtResults = strName
		message = font.render(txtResults, 1, cBLUE)
		screen.blit(message, (240-message.get_rect().width/2, 70))

		font = pygame.font.Font('/home/pi/PiTime/Antonio-Bold.ttf', 36)
		if (score >=10):
			txtResults = ' PERFECT !'
		elif (score >=7):
			txtResults = ' VERY GOOD !'
		elif (score >=5):
			txtResults = ' NOT BAD !'
		elif (score >=3):
			txtResults = ' BAD !'
		elif (score < 3):
			txtResults = ' DISASTROUS !'
		else:
			txtResults = ' ERROR !'
		message = font.render(txtResults, 1, cBLUE)
		screen.blit(message, (240-message.get_rect().width/2, 115))

		font = pygame.font.Font('/home/pi/PiTime/Antonio-Bold.ttf', 24)
		txtResults = 'You have succesfully answered ' + str(score) + ' of ' + str(NResponse) + ' questions'
		message = font.render(txtResults, 1, cBLUE)
		screen.blit(message, (240-message.get_rect().width/2, 185))
		txtResults = 'with a time of ' + str(segundos) + ' seconds.'
		message = font.render(txtResults, 1, cBLUE)
		screen.blit(message, (240-message.get_rect().width/2, 215))

		# Add the best and display the best 10
		# Show the best scores
		high_scores = {}
		if (os.path.exists('/home/pi/PiTime/HighScores.txt')) and (os.path.getsize('/home/pi/PiTime/HighScores.txt')>0):
			high_scores = json.load(open('/home/pi/PiTime/HighScores.txt'))
		else:
			high_scores = {}

		if len(high_scores) == 0:
			# Score table is empty, fill it
			array_scores = []
		else:
			array_scores = high_scores["list"]
		array_scores.append((strName,score,NResponse,secs,score*100/NResponse,secs/score))
		array_scores = sorted(sorted(sorted(array_scores, key=itemgetter(3), reverse=False), key=itemgetter(2), reverse=True), key=itemgetter(4), reverse=True)[:10]
		new_high_scores = {}
		new_high_scores["list"] = array_scores

		with open('/home/pi/PiTime/HighScores.txt', 'w') as outfile:
			json.dump(new_high_scores, outfile)

		# timer for screen
		Clock.tick(20)

		# Refresh the screen
		pygame.display.flip()

		pygame.mixer.music.load(Bef_Sound)
		pygame.mixer.music.play(0)
		pygame.mixer.music.load(Score_Sound)
		pygame.mixer.music.play(0)

		# Wait for button/user input
		PressedButton = -1
		Cont = True;
		while (Cont):
			if (PressedButton == red):
				PressedButton = -1
				present_phase = f_TOP
				Cont = False;

# end the game
pygame.quit()
