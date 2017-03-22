import os
import sys
import time
from PIL import Image
from PIL import ImageGrab
from playsound import playsound

from skimage.measure import structural_similarity as ssim
import matplotlib.pyplot as plt
import numpy as np
import cv2

# Sample code to load 1 buff image and compare against list of buff images to determine if buff is up!
# http://www.pyimagesearch.com/2014/09/15/python-compare-two-images/
# [Buffs are 32x32 squares]
def compare_images(imageA, imageB, title):
    s = ssim(imageA, imageB)

    # setup the figure
    fig = plt.figure(title)
    plt.suptitle('SSIM: %.2f' % (s))

    # show first image
    ax = fig.add_subplot(1, 2, 1)
    plt.imshow(imageA, cmap = plt.cm.gray)
    plt.axis('off')

    # show the second image
    ax = fig.add_subplot(1, 2, 2)
    plt.imshow(imageB, cmap = plt.cm.gray)
    plt.axis('off')

    # show the images
    plt.show()

# Load images:
original = cv2.imread('fishing_buff_icon.jpg')
desert_day = cv2.imread('desert_debuff_day_icon.JPG')
move_buff = cv2.imread('movement_buff_icon.jpg')
fishing_buff = cv2.imread('fishing_buff_icon.jpg')
gathering_buff = cv2.imread('gathering_buff_icon.jpg')
item_obtain_buff = cv2.imread('item_obtain_buff_icon.jpg')
desert_night = cv2.imread('desert_debuff_night_icon.JPG')

# convert the images to grayscale
original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
desert_day = cv2.cvtColor(desert_day, cv2.COLOR_BGR2GRAY)
move_buff = cv2.cvtColor(move_buff, cv2.COLOR_BGR2GRAY)
fishing_buff = cv2.cvtColor(fishing_buff, cv2.COLOR_BGR2GRAY)
gathering_buff = cv2.cvtColor(gathering_buff, cv2.COLOR_BGR2GRAY)
item_obtain_buff = cv2.cvtColor(item_obtain_buff, cv2.COLOR_BGR2GRAY)
desert_night = cv2.cvtColor(desert_night, cv2.COLOR_BGR2GRAY)

# compare the images
compare_images(original, desert_day, 'Original vs. Desert Day')
compare_images(original, move_buff, 'Original vs. Movement')
compare_images(original, fishing_buff, 'Original vs. Fishing')
compare_images(original, gathering_buff, 'Original vs. Gathering')
compare_images(original, item_obtain_buff, 'Original vs. Item Obtain')
compare_images(original, desert_night, 'Original vs. Desert Night')


# TEST MARKETPLACE NOTIFICATION ALERTS / EASIER THAN BUFF BOT?
# Code to grab buffs from screen / code to play sound:

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
