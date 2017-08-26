#!/usr/bin/env python3

'''
# *dumbphone* #

A Python program that runs (ideally on a server 24/7) for you to text for information
that you otherwise only get with a smart phone & data plan.

Twilio - (free trial) gives a phone number to text that essentially gets forwarded to your server

## Why: ##
- Smartphones = worst & I recently gave mine up
  - Current apps are designed to catch & keep our attention to deliver useless "content"
  - Too much screen time bad for mental health, memory, happiness
  - I made an attempt at designing a program to that performs some useful ("smart") functions but won't addict users



## Examples: ##

msg_response = DumbphoneResponse("goog seattle central library hours")
print(msg_response.dumbphone_responder())

example_list = ["maps, 110 vine street seattle wa, 2200 2nd ave seattle wa", "weather tomorrow",\
"goog seattle central library hours", "chariot las vegas", "tide", "sun", "cal 8/16", "goog translate aburguesamiento"]


for msg in example_list:
    print(msg+":\n")
    msg_response = DumbphoneResponse(msg)
    print(msg_response.dumbphone_responder())

# also: "limebike 1234" ... eventually


### to do: ###
- Come up with less dumb name than dumbphone - dumbnomo' as in dumb no more
- Clean up maps.py - make more concise by deleting repetitive code
- Limebike with different android emulator or some other solution -D/l and work android studio?
- fix all individual other todos
- Put on server/raspberry pi

All requirements:
python3
bs4
requests
urllib2
httplib2
oauth2client
apiclient
flask
twilio
#limebike requires:
bluestacks (or other android emulator)
pyautogui

'''
import weather
import chariot
import sunset
import maps
import my_calendar
import limebike
import googl
import help
import time

menu_options = "DumbPhone Menu:\n1.Weather\n2.Calendar\n3.Maps\n4.Limebike\n5.Chariot\n6.Tides\n7.Sun\n8.Goog"

# Takes SMS input to determine which functions should run
class DumbphoneResponse():
    def __init__(self, incoming_text):
        self.message_time = time.strftime("%c")
        self.incoming_text = incoming_text

    def dumbphone_responder(self):
        # Full text is the string argument for functions
        full_text = self.incoming_text.lower().strip()
        # Text is the first word, which chooses the function
        text = full_text.split(" ")[0]

        if text == "menu":
            respond_with = menu_options
        # Help either responds with menu options, or help for the specific menu function
        elif text == "help":
            if len(full_text.split(" "))<2:
                respond_with = menu_options
            else:
                respond_with = help.helperfunc(full_text.split(" ")[1])
        elif text[:1]=="1" or text[:1]=="w":
            respond_with = weather.weather_function(full_text)
        elif text[:1]=="2" or text[:3]=="cal":
            respond_with = my_calendar.main(full_text)
        elif text[:1]=="3" or text=="m" or text[:3]=="map":
            # Try because if the address doesn't work it'll throw an error!
            try:
                respond_with = maps.map_function(full_text)
            except:
                respond_with = "Address error, one or both of those addresses is fake."
        elif text[:1]=="4" or text[:4]=="lime" or text[:4]=="bike" or text[:4]=="spin":
            respond_with = limebike.limebike_unlock(full_text)
        elif text[:1]=="5" or text == "cab" or text=="chariot" or text=="taxi":
            chariot_text = " ".join(full_text.split()[1:])
            respond_with = chariot.main(chariot_text)
        elif text[:1]=="6" or text=="tides" or text=="tide" or text=="t":
            respond_with = sunset.sun_or_tides("t")
        elif text[:1]=="7" or text[:3]=="sun":
            respond_with = sunset.sun_or_tides("s")
        elif text[:1]=="8" or text[:4]=="goog" or text == "bing":
            search_query = " ".join(full_text.split(' ')[1:])
            respond_with = googl.get_answer(search_query)
        else:
            respond_with = "huh?\n"+menu_options

        # Write a log of messages to a .txt file
        with open("log.txt", "a") as f:
            f.write("({})\nMsg in:\n{}\n\nMsg out:\n{}\n\n".format(self.message_time, self.incoming_text, respond_with))
        return respond_with.strip()

