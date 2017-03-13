import os
import sys
import time
from PIL import Image
from PIL import ImageGrab
from playsound import playsound

# http://www.pyimagesearch.com/2014/09/15/python-compare-two-images/

#time.sleep(5)
#bbox=(400,800,700,1000)
#ImageGrab.grab(bbox).save('screen_capture.png')

'''
pix = im.load()
print im.size #Get the width and hight of the image for iterating over
print pix[17,40] #Get the RGBA Value of the a pixel of an image (x,y)

im_out = Image.new("RGB", (128, 128))
pix_out = im_out.load()
for x in range(128):
    for y in range(128):
        pix_out[x,y] = pix[17,40] #(255,0,0)

#im_out.save("test.png", "PNG")
im_out.show()
'''

#im = Image.open('desert_debuff_day.JPG')
# buffbar_day.JPG:
# (100,100): (194,172,135) | Sand
# (93,92): (199,175,139) | Sand

# desert_debuff_day.JPG:
# (8,45): (111,96,73) | Debuff border
# (17,40): (237,229,227) | Debuff, 1st M

'''
playsound('audio/sms_alert.mp3')
#playsound('audio/bomb_siren.mp3')
#playsound('audio/eas_beep.mp3')
'''
