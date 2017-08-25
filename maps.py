#!/usr/bin/env python3

'''
Googe maps text function

input (**, from, to, mode=bike)

-the function uses this to build a url using google maps' api then builds that into a list
So the default mode is bike, but otherwise you can bus, drive, etc.

**=maps, m etc.


to do:

- Get all optional modes to work. - now it's just transit/bus or defaults to bike.
- If one of the addresses isn't correct it crashes! - Currently fixed with try/except in dumbphone.py, but not here...
- Break up texts and send using send_sms.py


transit:
https://maps.googleapis.com/maps/api/directions/json?origin=+110+vine+street+seattle+wa&destination=+3416+Fremont+Ave+N+seattle+wa&mode=transit&key=AIzaSyB-V54J_vld1r8Ltt5jodbsUi6m155PP4s

walking:
https://maps.googleapis.com/maps/api/directions/json?origin=110+vine+street+seattle+wa&destination=3416+Fremont+Ave+N+seattle+wa&mode=driving&key=AIzaSyB-V54J_vld1r8Ltt5jodbsUi6m155PP4s


requires:
re
urllib
json
'''

import urllib.request, json
import re

file = open("mapsapikey.txt")
key = file.read()
file.close()



#It's all in one function at the moment, will split up when "Transit" option is added.
# takes a comma separated string with at least "maps, origin, destination" as input
# will eventually take 4th argument of mode of transit. Currently defaults to bike 'cause that's what I do.
def map_function(input_string):
    args = input_string.split(",")
    map_help = "Enter:\"m, origin, dest, mode.\" eg: \"m, 110 vine st seattle wa, fremont brewing company wa, transit.\"\
               \nNote: NO comma in address."
    if len(args) != 3 and len(args) != 4:
        return map_help

    #default is bicycling, otherwise use bus
    mode = "bicycling"
    if len(args) == 4:
        mode = args[3].lower().strip()
        if mode == "bus":
            mode = "transit"

    origin = "+".join(args[1].split(" "))
    destination = "+".join(args[2].split(" "))

    #the JSON url that is queried for directions
    maps_url = "https://maps.googleapis.com/maps/api/directions/json?origin="+origin+"&destination="+destination+"&mode="+mode+"&key="+key
    #print(maps_url)
    direction_list = []
    #commented out local file for testing...
    #with open('example.json') as data_file:
    if mode == "transit":
        with urllib.request.urlopen(maps_url) as url:
            data = json.loads(url.read().decode())
            i = 0
            while i < len(data["routes"][0]['legs'][0]['steps']):
                words = data["routes"][0]['legs'][0]['steps'][i]['html_instructions']
                words = re.sub('<div.*?</div>', '', words)
                try:
                    words += ". Bus #:{},".format(data["routes"][0]['legs'][0]['steps'][i]['transit_details']['line']['short_name'])
                    words += " ({} stops)".format(data["routes"][0]['legs'][0]['steps'][i]['transit_details']['num_stops'])
                    words += " to {})".format(data["routes"][0]['legs'][0]['steps'][i]['transit_details']['arrival_stop']['name'])

                except:
                    pass

                # Get rid of html tags, regex credit:
                # https://stackoverflow.com/questions/753052/strip-html-from-strings-in-python
                directions = re.sub('<[^<]+?>', '', words)

                direction_list.append(directions)
                i+=1
        a=0
        all_directions = ""
        while a < len(direction_list):
            all_directions += (str(a+1)+". "+direction_list[a]+"\n")
            a+=1

        """
        # so, next we'll split up 
        string_pos = 0
        while string_pos<len(all_directions):
            try:
                string_pos += 140
                print(all_directions[:string_pos])
            except:
                string_pos+=140
                print(all_directions[string_pos:len(all_directions)])
        """
        return all_directions
    # If not transit, bike!
    else:
        with urllib.request.urlopen(maps_url) as url:
            # data = json.load(data_file)
            data = json.loads(url.read().decode())
            i = 0
            while i < len(data["routes"][0]['legs'][0]['steps']):
                # html written directions, thanks Google!
                words = data["routes"][0]['legs'][0]['steps'][i]['html_instructions']
                # distance you have to go until doing the nxt direction
                distance = data["routes"][0]['legs'][0]['steps'][i]['distance']['text']
                # get rid of annoying text that's in some sets of directions,
                # but the last one tells us which side the destination is on, so we'll save that and use it later
                if i != (len(data["routes"][0]['legs'][0]['steps']) - 1):
                    words = re.sub('<div.*?</div>', '', words)
                    directions = words + ". Then go " + distance + "."
                else:
                    end = re.search('<div.*?</div>', words).group(0)
                    words = re.sub('<div.*?</div>', '', words)
                    directions = words + ". Then go " + distance + ". " + end + "."

                # Get rid of html tags, regex credit:
                # https://stackoverflow.com/questions/753052/strip-html-from-strings-in-python
                directions = re.sub('<[^<]+?>', '', directions)

                direction_list.append(directions)
                i += 1
        a = 0
        all_directions = ""
        while a < len(direction_list):
            all_directions += (str(a + 1) + ". " + direction_list[a] + "\n")
            a += 1
        return all_directions