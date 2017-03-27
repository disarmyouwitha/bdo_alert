import os
import sys
import cv2
import time
import numpy
import PIL.ImageOps
from PIL import Image
from PIL import ImageGrab
from PIL import ImageEnhance
from readbot import ReadBot
from playsound import playsound
from twisted.internet import task
from twisted.internet import reactor
from skimage.measure import structural_similarity as ssim

# http://www.pyimagesearch.com/2014/09/15/python-compare-two-images/

cnt = 0
known_buffs = {}
energy_buffer = []

def load_known_buffs():
    desert_day = cv2.imread('buff_icons/desert_debuff_day_icon.JPG')
    desert_night = cv2.imread('buff_icons/desert_debuff_night_icon.JPG')
    movement_buff = cv2.imread('buff_icons/movement_buff_icon.jpg')
    fishing_buff = cv2.imread('buff_icons/fishing_buff_icon.jpg')
    gathering_buff = cv2.imread('buff_icons/gathering_buff_icon.jpg')
    item_obtain_buff = cv2.imread('buff_icons/item_obtain_buff_icon.jpg')
    weight_buff = cv2.imread('buff_icons/weight_buff_icon.jpg')
    energy_recovery_buff = cv2.imread('buff_icons/energy_recovery_buff_icon.jpg')

    # convert the images to grayscale
    _desert_day = cv2.cvtColor(desert_day, cv2.COLOR_BGR2GRAY)
    _desert_night = cv2.cvtColor(desert_night, cv2.COLOR_BGR2GRAY)
    _movement_buff = cv2.cvtColor(movement_buff, cv2.COLOR_BGR2GRAY)
    _fishing_buff = cv2.cvtColor(fishing_buff, cv2.COLOR_BGR2GRAY)
    _gathering_buff = cv2.cvtColor(gathering_buff, cv2.COLOR_BGR2GRAY)
    _item_obtain_buff = cv2.cvtColor(item_obtain_buff, cv2.COLOR_BGR2GRAY)
    _weight_buff = cv2.cvtColor(weight_buff, cv2.COLOR_BGR2GRAY)
    _energy_recovery_buff = cv2.cvtColor(energy_recovery_buff, cv2.COLOR_BGR2GRAY)

    global known_buffs
    known_buffs['desert_day'] = _desert_day
    known_buffs['desert_night'] = _desert_night
    known_buffs['movement_buff'] = _movement_buff
    known_buffs['fishing_buff'] = _fishing_buff
    known_buffs['gathering_buff'] = _gathering_buff
    known_buffs['item_obtain_buff'] = _item_obtain_buff
    known_buffs['weight_buff'] = _weight_buff
    known_buffs['energy_recovery'] = _energy_recovery_buff

def compare_buffs(buff_a, buff_b):
    s = ssim(buff_a, buff_b)
    #print '%.2f' % s
    return s

def return_buff(unknown_buff, success_threshold=.8, debug=False):
    _meets_threshold = {}

    for buff_name, buff_icon in known_buffs.iteritems():
        _buff_ssim = compare_buffs(unknown_buff, buff_icon)
        if _buff_ssim >= success_threshold:
            _meets_threshold[buff_name] = _buff_ssim

    if len(_meets_threshold) == 1:
        return _meets_threshold.items()[0]
    else:
        if debug == True:
            print _meets_threshold
            # determine highest && return?
        else:
            return ('err', 'no buff matched')


def read_buff_bar(_buff_bar):
    size = 32
    offset_x = 0
    offset_y = 0
    buff_spacing = 33
    active_buffs = []

    # Read active buffs:
    _done = False
    while _done == False:
        _buff_bounds = (offset_x, offset_y, offset_x+size, offset_y+size)
        _buff_box = _buff_bar.crop(_buff_bounds)
        #_buff_box.show()
        #sys.exit(1)

        # Convert from PIL to CV2 image:
        pil_buff = _buff_box.convert('RGB')
        open_cv_buff = numpy.array(pil_buff)

        # Convert from RGB to BGR / GRAYscale:
        open_cv_buff = open_cv_buff[:, :, ::-1].copy()
        _unknown_buff = cv2.cvtColor(open_cv_buff, cv2.COLOR_BGR2GRAY)

        (buff_name, buff_ssim) = return_buff(_unknown_buff)
        #print '%s | %s' % (buff_name, buff_ssim)

        if buff_name == 'err':
            _done = True
        else:
            active_buffs.append(buff_name)
            offset_x += buff_spacing

    return active_buffs

def read_debuff_bar(_buff_bar):
    size = 32
    offset_x = 0
    offset_y = 54
    buff_spacing = 33
    active_debuffs = []

    # Read active buffs:
    _done = False
    while _done == False:
        _buff_bounds = (offset_x, offset_y, offset_x+size, offset_y+size)
        _buff_box = _buff_bar.crop(_buff_bounds)
        #_buff_box.show()
        #sys.exit(1)

        # Convert from PIL to CV2 image:
        pil_buff = _buff_box.convert('RGB')
        open_cv_buff = numpy.array(pil_buff)

        # Convert from RGB to BGR / GRAYscale:
        open_cv_buff = open_cv_buff[:, :, ::-1].copy()
        _unknown_buff = cv2.cvtColor(open_cv_buff, cv2.COLOR_BGR2GRAY)

        (buff_name, buff_ssim) = return_buff(_unknown_buff)
        #print '%s | %s' % (buff_name, buff_ssim)

        if buff_name == 'err':
            _done = True
        else:
            active_debuffs.append(buff_name)
            offset_x += buff_spacing

    return active_debuffs

def screen_grab_health_bar():
    # 1920 x 1200, windowed mode:
    offset_x = 657
    offset_y = 949
    box_width = 300
    box_height= 103

    # Code to ImageGrab screenshot of buffs/debuff bounds.. pass to reader functions:
    bbox=(offset_x, offset_y, offset_x+box_width, offset_y+box_height)
    ImageGrab.grab(bbox).save('screen_capture_hp.png')
    hp_bar = Image.open('screen_capture_hp.png')
    #hp_bar.show()
    #sys.exit(1)

def screen_grab_energy_bar():
    # 1920 x 1200, windowed mode:
    offset_x = 128
    offset_y = 81
    box_width = 30
    box_height= 15

    # Code to ImageGrab screenshot of buffs/debuff bounds.. pass to reader functions:
    bbox=(offset_x, offset_y, offset_x+box_width, offset_y+box_height)
    ImageGrab.grab(bbox).save('screen_capture_energy.png')

    # Convert to grayscale:
    im = Image.open('screen_capture_energy.png')
    imG = im.convert('L')
    imG.save('screen_capture_energy_gray.png')

    #energy_bar = cv2.cvtColor(cv2.imread('screen_capture_energy.png'), cv2.COLOR_BGR2GRAY)
    #cv2.imwrite('screen_capture_energy_gray.png', energy_bar)

    rb = ReadBot(digits_only=True)
    energy_str = rb.interpret('screen_capture_energy_gray.png')

    #print energy_str
    with open('energy_log.log', 'a') as f:
    	f.write(energy_str+'\n')

    return energy_str

def screen_grab_buff_box():
    # 1920 x 1200, windowed mode:
    offset_x = 657
    offset_y = 949
    box_width = 300
    box_height= 103

    # Code to ImageGrab screenshot of buffs/debuff bounds.. pass to reader functions:
    bbox=(offset_x, offset_y, offset_x+box_width, offset_y+box_height)
    ImageGrab.grab(bbox).save('screen_capture.png')
    buff_bar = Image.open('screen_capture.png')
    #buff_bar.show()
    #sys.exit(1)

    # Read buffs/debuffs:
    active_buffs = read_buff_bar(buff_bar)
    active_debuffs = read_debuff_bar(buff_bar)

    # Print them out for test..
    #print active_buffs
    print active_debuffs

    # Or play a sound if a certain buff is active:
    if len(active_debuffs) > 0:
        if 'desert_day' or 'desert_night' in active_debuffs:
            print '[playing audio]'
            playsound('audio/eas_beep.mp3')
            #playsound('audio/sms_alert.mp3')
            #playsound('audio/bomb_siren.mp3')

def screen_grab_manager():
    global cnt, energy_buffer

    # Run every tick:
    screen_grab_buff_box()

    # Run every other tick:
    if cnt%2==0:
        energy_str = screen_grab_energy_bar()

        if len(energy_buffer) > 3:
            energy_buffer.pop(0)

        energy_buffer.append(energy_str)
        print energy_buffer

        # Check energy_buffer for static energy:
        _all_same = True
        _first_energy = None
        for energy in energy_buffer:
            if _first_energy == None:
                _first_energy = energy
            else:
                if energy != _first_energy:
                    _all_same = False

        if len(energy_buffer) > 3 and _all_same == True and _all_same is not None:
            playsound('audio/sms_alert.mp3')
        # Check rising energy (threshold ~5)


    #print cnt
    cnt+=1

if __name__ == '__main__':
    load_known_buffs()

    l = task.LoopingCall(screen_grab_manager)
    l.start(5) # call every x seconds
    reactor.run()
