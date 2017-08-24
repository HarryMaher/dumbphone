#!/usr/bin/env python3

'''
Weather function

Gives a the text weather forecast. Defaults to today if no argument given. So "tomorrow" is really the only useful argument.

example input: weather_function("tomorrow"):
output:        Saturday: Mainly sunny. High 86F. Winds WSW at 5 to 10 mph. Saturday Night: Clear. Low 63F. Winds N at 5 to 10 mph.

to do:
save api key elsewhere...


requires:
re
urllib
json
'''

import re
import urllib.request, json
file = open("weatherapikey.txt")
api_key = file.read()
file.close()

# The chopping block takes off parts that make it too long. Ideally shortening it to a single text.
def chopping_block(text):
    if len(text) > 55:
        # winds are pretty local so this is the first to be removed for brevity...
        text = re.sub(" Winds.+?\.", '', text)
    if len(text) > 55:
        # the first sentence always talks about clouds, which aren't too important to me either.
        text = re.sub("^.+?\. ", '', text)
    return text

# The weather function gives today's weather or tomorrow's if you specify "tom"
# returns specified day's weather and gives current temp.
def weather_function(input_str):
    day = "today"
    if len(input_str.split(" ")) > 1:
        day = input_str.split(" ")[1]
    if day[:3] == "tom":
        start = 2
    else:
        start = 0
    weather_url = "http://api.wunderground.com/api/"+api_key+"/forecast10day/q/WA/Seattle.json"
    current_temp_url = "http://api.wunderground.com/api/"+api_key+"/conditions/q/WA/Seattle.json"

    with urllib.request.urlopen(weather_url) as url:
        parsed_json = json.loads(url.read().decode())
        title = day.capitalize()
        txt = parsed_json['forecast']['txt_forecast']['forecastday'][start]['fcttext']
        try:
            title2 = parsed_json['forecast']['txt_forecast']['forecastday'][start+1]['title'].split(" ")[1]
        except:
            title2 = parsed_json['forecast']['txt_forecast']['forecastday'][start+1]['title']
        txt2 = parsed_json['forecast']['txt_forecast']['forecastday'][start+1]['fcttext']

    with urllib.request.urlopen(current_temp_url) as url2:
        parsed_json2 = json.loads(url2.read().decode())
        current_temp = parsed_json2['current_observation']['temp_f']
        current_temp = int(current_temp)

    txt = chopping_block(txt)
    txt2 = chopping_block(txt2)
    full_forecast = "{}f. {}: {}\n{}: {}".format(current_temp, title, txt, title2, txt2)
    return full_forecast