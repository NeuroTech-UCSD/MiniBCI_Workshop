import pyautogui
from Threshold import Threshold
import time
threshold = Threshold()
threshold.get_signal()
threshold.set_pull()
threshold.calibrate()

time.sleep(3)
key = ''
while True:
    time.sleep(0.2)
    new_key = threshold.listen()

    if(key == ''):
        key = new_key
        continue
    elif (key == new_key):
        continue
    elif(key != new_key):
        pyautogui.keyUp(key)
        key = new_key
        pyautogui.keyDown(key)
    else:
        print('Key error')

