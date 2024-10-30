import pyautogui
from Threshold import Threshold
import time
import yaml

def run_controller(calibrate):
    threshold = Threshold()
    threshold.get_signal()

    if calibrate == 1:
        threshold.calibrate()
    else:
        with open("config.yml") as file:
            try:
                yaml_values = yaml.safe_load(file)
                threshold.relax_mean = yaml_values['relax_mean']
                threshold.flex_mean = yaml_values['flex_mean']
                threshold.temp_threshold = yaml_values['temp_threshold']
            except yaml.YAMLError as exc:
                print(exc)

    print('Start the game!')
    time.sleep(5)

    #initialize key and counter variable to track how many times a different key is read
    key = 'right'
    new_key_count = 0
    while True:
        time.sleep(0.1)
        next_key = threshold.listen()

        # if(key == ''):
        #     key = next_key
        #     continue
        if (key == next_key):
            continue
        elif(key != next_key):
            new_key_count += 1
            if(new_key_count == 6):
                pyautogui.keyUp(key)
                key = next_key
                pyautogui.keyDown(key)
                new_key_count = 0
        else:
            print('Key error')
        

run_controller(calibrate=0)
