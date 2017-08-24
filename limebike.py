#!/usr/bin/python

'''
Limebike

Limebike is a local stationless bikeshare program. It requires a smartphone to use.
This script lets you unlock a bike when you text it a 6 digit code.

Just lock the bike up to finish your ride.

$1/30 mins

To do:
-Get a spin app that won't crash in bluestack's emulator
-figure out how to get emulator to load more quickly?
-if updates pop up ?!?


!!!!!
#Note: you will need to change the numbers to fit the resolution of your screen
# use pyautogui.position() to find current mouse position!
# and change when bluestacks or limebikes put out any updates...
# Info in this tutorial: https://automatetheboringstuff.com/chapter18/
!!!!!

!!!!!
Requires:
Install bluestacks on your computer, log into android on it and install the limebike app.
 - set up your credit card and put rides on your account.
Put screenshots of the places it'll click in the apps in an "images" folder in this directory!
python3
pyautogui
!!!!!
'''
import pyautogui
import time
import send_sms

#This unlocks the bike - should work most of the time.
def unlock_function(input_string):
    lime_help = "Enter: \"limebike bikenumber. No other spaces or funny business\" eg: \"lime 123456\". Just those two!\n"
    args = input_string.split(" ")
    while len(args) != 2:
        return lime_help
    bike_number = input_string.split(" ")[1]
    # change this to the screen coordinates of your start menu or app search function.
    pyautogui.click(22, 746)
    time.sleep(.3)
    pyautogui.typewrite("bluestacks\n")
    time.sleep(15)
    pyautogui.click(pyautogui.center(pyautogui.locateOnScreen("images/myAppsToClick.png")))
    while pyautogui.locateOnScreen("images/limebike.png") == None:
        time.sleep(2)
    pyautogui.click(pyautogui.center(pyautogui.locateOnScreen("images/limebike.png")))
    time.sleep(1)
    while pyautogui.locateOnScreen("images/unlock.png") == None:
        time.sleep(.5)
    pyautogui.click(pyautogui.center(pyautogui.locateOnScreen("images/unlock.png")))
    time.sleep(.2)
    pyautogui.click()
    time.sleep(1)
    while pyautogui.locateOnScreen("images/typeDigitsOption.png") == None:
        time.sleep(.3)
    pyautogui.click(pyautogui.center(pyautogui.locateOnScreen("images/typeDigitsOption.png")))
    time.sleep(.2)
    pyautogui.click()
    time.sleep(1)
    while pyautogui.locateOnScreen("images/typeDigits.png") == None:
        time.sleep(.3)
    pyautogui.click(pyautogui.center(pyautogui.locateOnScreen("images/typeDigits.png")))
    time.sleep(.2)
    pyautogui.click()
    time.sleep(.2)
    pyautogui.typewrite(str(bike_number))
    time.sleep(4)
    if pyautogui.locateOnScreen("images/failed.png") != None:
        pyautogui.click(pyautogui.center(pyautogui.locateOnScreen("images/failedOk.png")))
        text_return = "Failed. Bike under maintenance, sorry try another bike :(..."
        send_sms.send_message(text_return)
    else:
        text_return = "Unlocking bike..."
        send_sms.send_message(text_return)
    pyautogui.click(pyautogui.center(pyautogui.locateOnScreen("images/limeClose.png")))
    time.sleep(1)
    pyautogui.click(pyautogui.center(pyautogui.locateOnScreen("images/appCenter.png")))
    return text_return

# Sometimes the android emulator pops up an advertisement. This waits for 10 seconds
# (because the ad has to display for 10 sec) then closes the ad.

def close_ad_function():
    time.sleep(10)
    pyautogui.click(pyautogui.center(pyautogui.locateOnScreen("images/removeAdsX.png")))


def limebike_unlock(input_string):
    try:
        return unlock_function(input_string)
    except:
        try:
            close_ad_function()
            return unlock_function(input_string)
        except:
            text_return = "Sorry there was an issue with the computer :("
            send_sms.send_message(text_return)


