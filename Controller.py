import pyautogui
from Threshold import Threshold

threshold = Threshold()
threshold.get_signal()
threshold.set_pull()
threshold.calibrate()


while True:
    key = threshold.listen()
    pyautogui.keyDown(key)

