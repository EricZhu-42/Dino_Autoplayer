import time
from PIL import ImageGrab
from PIL import Image

import win32api,win32con

while True:
    raw_pic = ImageGrab.grab()
    pic = raw_pic.load()
    color_dino = pic[73,473]

    start_point = 440
    end_point = 486

    for y in range(start_point,end_point):
        if pic[290,y]==color_dino:
            win32api.keybd_event(32, 0, 0, 0)
            win32api.keybd_event(32, 0, win32con.KEYEVENTF_KEYUP, 0)
            time.sleep(0.60)
            break

