import numpy as np
import cv2
from PIL import ImageGrab, Image
import pyautogui
import time


def PIDOR():
    pyautogui.moveTo(500, 300)
    pyautogui.mouseDown(button='left')
    time.sleep(1)
    pyautogui.moveTo(400, 100)
    pyautogui.mouseUp(button='left')

def JOPA():
    image = np.array(ImageGrab.grab(bbox=(450, 260, 490, 310)))
    red_dominant = (image[:, :, 0] > image[:, :, 1]) & (image[:, :, 0] > image[:, :, 2])
    return np.sum(red_dominant) / red_dominant.size * 100

CON = 0
def HUETA():

        CON = 0
        screenshot = ImageGrab.grab(bbox=(800, 470, 1300, 700))
        
        template = Image.open("image.png")

        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2RGB).astype(np.uint8)
        template = cv2.cvtColor(np.array(template), cv2.COLOR_BGR2RGB).astype(np.uint8)

        
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val > 0.4:
            CON = 1
            top_left = max_loc
            object_x_position = top_left[0]

            if object_x_position < 130:
                print(object_x_position, "yes")
                pyautogui.mouseDown(button='left')
            else:
                print(object_x_position, "no")
                pyautogui.mouseUp(button='left')

        print(CON)



def BLYADINA():
     PIDOR()
     while True:

        print(JOPA())
        if 2<JOPA()<10:
             print("GO")
             pyautogui.mouseDown(button='left')
             pyautogui.mouseUp(button='left')
         
        HUETA()



