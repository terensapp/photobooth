from PIL import Image
from os import system

im = Image.open('xmas/newstage.jpg')
pix = im.load()
width,height = im.size
print width
print height
print '#%02x%02x%02x' % pix[50,50]
im = Image.open('newimage.png')
pix = im.load()
green = '#%02x%02x%02x' % pix[50,50]
green2 = '#%02x%02x%02x' % pix[300,50]
print green
print green2
