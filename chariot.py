#!/usr/bin/env python3

'''

Chariot

Goog scraper that just performs a google maps search for cab in X city.
This is for educational purposes so also don't sue me. Thanks :)

Optional parameter = city. Default is Seattle.

Returns (3x):
company-rating-phone number

to do:
nothing really. Maybe optimize regex?
If Google ever changes, change the class from _axi to whatever it is.

requires:
python3
bs4
requests
'''


import requests
import re
from bs4 import BeautifulSoup

#A simple web scraping function - generates a generic google search and scrapes it based on the input
def main(city="Seattle"):
    #Dunno why I prefer this to .replace()...
    city_query = "+".join(city.split(" "))
    url = "https://www.google.com/search?q=cab+"+city_query

    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, "lxml")
    all_tags = soup.find_all("a", {"class": "_axi"})
    all_companies = ""
    if len(all_tags) == 0:
        apologies = "Sorry, {} might need a state name too, or is small, or spelled wrong or something :/".format(city)
        return apologies
    for t in all_tags:
        t = re.sub('<span class="_PXi">', "-", str(t))
        t = re.sub('<div class="rllt__wrapped">.+?>', "",t)
        t = re.sub('</span> <g-review-stars>.+?</div><div></div><div>.+?\(', "-(",t)
        t = re.sub('<[^<]+?>', '', t)
        t = ")".join(t.split(") "))
        all_companies += "{}\n".format(t)
    all_companies = all_companies[:140]
    return all_companies

