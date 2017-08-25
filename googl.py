#!/usr/bin/python

'''
Bing answers scraper


Gives the first 140 chars of the automatic answer that bing gives when you look something up, not unlike the google answers one

To do:
It converts measures (distances, weights,) but it doesn't work for currencies...


Example uses:
print(get_answer("translate aburguesamiento"))
print(get_answer("define frumenty"))
print(get_answer("UW continuing education address"))
print(get_answer("who was the 13th president?"))
print(get_answer("Seattle Central Library hours today"))
print(get_answer("what is 25 feet in meters?"))
print(get_answer("fan etf price"))
print(get_answer("flight info NH177"))


'''
import requests
from bs4 import BeautifulSoup
import re

# Takes a search query and uses it on a search engine, scrapes and returns the 'quick answer' box
def get_answer(query):
    search = query.replace(" ","+")
    url= "http://www.bing.com/search?q="+search
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, "lxml")
    tag = soup.find("li", {"class": "b_top"})

    tag = str(tag)
    #clean everything up...
    original_tag = tag
    #Keep these chars https://stackoverflow.com/questions/27938765/replace-non-alphanumeric-characters-except-some-exceptions-python
    keepchars = "= "

    tag = re.sub('Larger map', '', tag)
    tag = re.sub('<select.+?</select>', '', tag)
    tag = re.sub('</div>', ' ', tag)
    tag = re.sub('</td>', ' ', tag)
    tag = re.sub('</input>', ' ', tag)
    tag = re.sub('<[^<]+?>', '', tag)
    tag = re.sub('Sorry.+?less', '', tag)
    tag = re.sub('Try.+?Edit', '', tag)
    tag = re.sub(r'[^a-zA-Z0-9=\/\-\:\.\" ]', '', tag)
    tag = re.sub('\ \-\ ', '-', tag)
    res = ' '.join(tag.split())

    # The unit converter requires that you extract the value from a textbox!
    # So it starts all over. Not the most efficient, but works for now...
    if tag[:13]=="Convert units":
        res = re.sub('<input class=\"ctxt b_focusTextMedium.+?value=\"','',original_tag)
        res = re.sub('"/>','',res)
        res = re.sub('<select.+?</select>', '', res)
        res = re.sub('</div>', ' ', res)
        res = re.sub('</td>', ' ', res)
        res = re.sub('</input>', ' ', res)
        res = re.sub('<[^<]+?>', '', res)
        res = re.sub('Sorry.+?less', '', res)
        res = re.sub('Try.+?Edit', '', res)
        res = re.sub(r'[^a-zA-Z0-9\/\-\:\.\" ]', '', res)
        res = re.sub('\ \-\ ', '-', res)
        res = ' '.join(res.split())
        return res[0:140]
    else:
        return res[0:140]