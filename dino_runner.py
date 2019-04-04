import time

import cv2 as cv
import numpy as np
import win32con
from PIL import ImageGrab
from PIL import Image

import win32api

def get_pixel(image,x=300,y=200):
    new_image = image.load()
    return new_image[x,y]

def init_background():
    raw_pic = np.asarray(ImageGrab.grab())
    return cv.cvtColor(raw_pic, cv.COLOR_BGR2GRAY)

def play(background,current_mode):
    screenshot = ImageGrab.grab()
    raw_pic = np.asarray(screenshot)
    gray_pic = cv.cvtColor(raw_pic, cv.COLOR_BGR2GRAY)

    difference = cv.absdiff(background, gray_pic)
    difference = cv.threshold(difference, 100, 255, cv.THRESH_BINARY)[1]

    contours, hierarchy = cv.findContours(difference.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    for c in contours:
        (x, y, width, height) = cv.boundingRect(c)

        if height <30 or y+height<430 or y >520 or x<110:
            continue

        if x<230 or (x<280 and y+height>440):
            win32api.keybd_event(32, 0, 0, 0)
            if height>50:
                time.sleep(0.2)
            win32api.keybd_event(32, 0, win32con.KEYEVENTF_KEYUP, 0)

        cv.rectangle(raw_pic, (x, y), (x+width, y+height), (0, 255, 0), 2)

    if current_mode=='day':
        change_condition = (0, 0, 0)
    else:
        change_condition = (255, 255, 255)

    if get_pixel(screenshot)==change_condition:
        global mode
        if mode=='day':
            mode = 'night'
        else:
            mode = 'day'

    cv.imshow('Targets', raw_pic)
    cv.waitKey(1)

background = None
mode = 'day'

if __name__ == "__main__":

    for i in range(0,10):
        print("{:.1f}s left!".format(2.0-0.2*i))
        time.sleep(0.2)

    while True:
        print("It's day!")
        background = init_background()
        while mode=='day':
            play(background,mode)
        print("It's night!")
        background = init_background()
        while mode=='night':
            play(background,mode)

    cv.destroyAllWindows()
