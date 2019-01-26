#!/usr/bin/python

import RPi.GPIO as GPIO
from picamera import PiCamera
from time import sleep
from os import system
import Adafruit_CharLCD as LCD
from datetime import datetime
from shutil import copyfile
from PIL import Image
import sys



pictime = sys.argv[2]
raw = "/storage/files/Photobooth/raw/"+pictime+"-raw.jpg"
processed = "/storage/files/Photobooth/final/"+pictime+".png"
copyfile(raw,'image.jpg')
fuzz = sys.argv[1]

system("rm -rf "+processed)
system("convert image.jpg -resize 480x336! -quality 100 newimage.png")
# Remove Green Screen
im = Image.open('newimage.png')
pix = im.load()
green = '#%02x%02x%02x' % pix[15,15]
green2 = '#%02x%02x%02x' % pix[300,15]
if green == green2:
  green2 = '#%02x%02x%02x' % pix[15,300]
  print("Trying to get a different green...")
chromacommand = 'convert newimage.png -fuzz '+fuzz+'% -transparent "'+green+'" out-chroma1.png'
print(chromacommand)
system(chromacommand)
# Second Pass
chromacommand = 'convert out-chroma1.png -fuzz '+fuzz+'% -transparent "'+green2+'" out.png'
print(chromacommand)
system(chromacommand)
system("convert moon.jpg out.png -flatten images/result.png")
copyfile('images/result.png',processed)
