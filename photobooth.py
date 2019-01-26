#!/usr/bin/python

import RPi.GPIO as GPIO
from picamera import PiCamera
from time import sleep
from os import system
import Adafruit_CharLCD as LCD
from datetime import datetime
from shutil import copyfile
from PIL import Image

greenscreen = 'yes'
printing = 'no'
fuzz = '12'
BUTTON_PIN = 26
DEBOUNCE = 0.05
	
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

camera = PiCamera()

# Raspberry Pi pin configuration:
lcd_rs        = 27  # Note this might need to be changed to 21 for older revision Pi's.
lcd_en        = 22
lcd_d4        = 25
lcd_d5        = 24
lcd_d6        = 23
lcd_d7        = 18
lcd_backlight = 4

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows    = 2

# Alternatively specify a 20x4 LCD.
# lcd_columns = 20
# lcd_rows    = 4

# Initialize the LCD using the pins above.
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_backlight)

lcd.clear()
lcd.message('Push The Button\nTo Start')

while True:
  if GPIO.input(BUTTON_PIN) == False:
    lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_backlight)
    lcd.clear()
    lcd.message('Strike a Pose\nAnd Freeze!')
    sleep(2)
    lcd.clear()
    lcd.message('Smile!\nPicture in 3..')
    sleep(1)
    lcd.clear()
    lcd.message('Smile!\nPicture in 2..')
    sleep(1)
    lcd.clear()
    lcd.message('Smile!\nPicture in 1..')
    sleep(1)
    lcd.clear()
    lcd.message('Say Cheese!!!\nStay Still...')
    camera.start_preview()
    sleep(2)
    camera.capture('/home/pi/photobooth/image.jpg')
    lcd.clear()
    lcd.message('OK Relax!\nGetting Olaf..')
    pictime = datetime.now().strftime("%Y%m%d-%H%M%S")
    raw = "/storage/files/Photobooth/raw/"+pictime+"-raw.jpg"
    camera.stop_preview()
    if(greenscreen == 'yes'):
      #system("convert image.jpg -resize 480x336! -quality 100 newimage.png")
      system("/home/pi/photobooth/squareup -s 480 -m crop -g Center image.jpg newimage.png")
      copyfile('/home/pi/photobooth/newimage.png',raw)
      # Remove Green Screen
      im = Image.open('newimage.png')
      pix = im.load()
      green = '#%02x%02x%02x' % pix[15,15]
      green2 = '#%02x%02x%02x' % pix[300,15]
      if green == green2:
        green2 = '#%02x%02x%02x' % pix[50,300]
        print("Trying to get a different green...")
      chromacommand = 'convert newimage.png -fuzz '+fuzz+'% -transparent "'+green+'" out-chroma1.png'
      print(chromacommand)
      system(chromacommand)
      # Second Pass
      chromacommand = 'convert out-chroma1.png -fuzz '+fuzz+'% -transparent "'+green2+'" out.png'
      print(chromacommand)
      system(chromacommand)
      system("convert -gravity south xmas/olaf.jpg out.png -composite images/result.png")
      #resize for ballroom
      system("convert out.png -resize 75% out75.png")
      system("convert -gravity south xmas/ballroom.jpg out75.png -composite images/result2.png")
      #system("convert out.png -resize 40% out40.png")
      system("convert -gravity south xmas/stage.jpg out75.png -composite images/result3.png")
      processed = "/storage/files/Photobooth/final/"+pictime+"-olaf.png"
      processed2 = "/storage/files/Photobooth/final/"+pictime+"-ballroom.png"
      processed3 = "/storage/files/Photobooth/final/"+pictime+"-stage.png"
      copyfile('images/result.png',processed)
      copyfile('images/result2.png',processed2)
      copyfile('images/result3.png',processed3)
      copyfile('images/result.png','/storage/files/Photobooth/result1.png')
      copyfile('images/result2.png','/storage/files/Photobooth/result2.png')
      copyfile('images/result3.png','/storage/files/Photobooth/result3.png')
      if printing == 'yes':
        system("pdflatex print.tex")
        system("/usr/bin/lp /home/pi/photobooth/print.pdf")
    else:
      if printing == 'yes':
        system("/usr/bin/lp /home/pi/photobooth/image.jpg")
    lcd.clear()
    lcd.message('Got Him!!\nPhotos Done!')
    #system("rm -rf image.jpg")
    #system("rm -rf newimage.png")
    #system("rm -rf out.pdf")
    sleep(10)
    lcd.clear()
    lcd.message('Push The Button\nTo Start')
  sleep(.5)
