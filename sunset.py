#!/usr/bin/python

'''
sunset.py does both
Sunset and Tides.

Gives next sunrise/sunset in Seattle.
Or gives tide information for downtown Seattle today.

To do:
Future versions can look for other days and by "friday" or "next friday" for Shabbat!

'''
import time
import requests
import re
from bs4 import BeautifulSoup


#this gives you current date:
#print(time.strftime("%A, %B %d, %Y"))

# use this for both sunset and tides information:
# http://www.tides.net/washington/2442/

# searches for the content that contains both the sunset and tide information for given day
def search():
    date = int(time.strftime("%d"))
    yr, mo = time.strftime("%Y"), time.strftime("%m")
    url= "http://www.tides.net/washington/2442/?year="+yr+"&month="+mo
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, "lxml")
    all_tags = soup.find_all("div", {"class": "wrap_textual_details"})
    return date, all_tags

def get_sunset(date,all_tags):
    sunsets = []
    for t in all_tags:
        string = ""
        string +="Sunrise: {}".format(str(t).split("-")[0][-6:])+'\n'
        string +="Sunset: {}".format(str(t).split("-")[1][:6])
        sunsets.append(string)
    this_sunset = sunsets[(date-1)]
    return this_sunset


#tides
# Splitting by periods and putting everything after "8:30pm" into a list then joining everything
# back up by periods (because those periods are decimal points in feet of the tides).
# Then put in newlines to add legibility and put in a colon after tide for good measure.
# example = "Wednesday, August 9, 2017. Sun 5:57am-8:30pm. low tide 12:49am (5.28ft), high tide 6:03am (9.89ft), low tide 12:41pm (-0.70ft), high tide 7:34pm (11.54ft)"
# print(".".join(example.split(".")[2:]).replace(", ", "\n").replace("tide", "tide:").strip())
def get_tides(date, all_tags):
    tides = []
    for t in all_tags:
        string = ".".join(str(t).split(".")[2:]).replace(", ", "\n").replace("tide", "tide:").strip()
        string = re.sub('<[^<]+?>', '', string).replace("high","High").replace("low","Low")
        tides.append(string)
    these_tides = tides[(date-1)]
    return these_tides

# Puts all the above functionality together to return the requested information, either tide or sunset.
def sun_or_tides(choice):
    date, all_tags = search()
    if choice == "s":
        text_this = get_sunset(date, all_tags)
    else:
        text_this = get_tides(date, all_tags)
    return text_this
