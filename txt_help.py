#!/usr/bin/env python3

'''
Help for dumbphone!

A dictionary of help for the dumbphone


'''

help_dict = {"weather":"\"Weather\" for today's forecast. \"weather tomorrow\" for tomorrow's. 1st number always current temp.",\
             "chariot":"\"Chariot Detroit\" returns cab company-rating-phone#. If no city, defaults to Seattle.",\
             "tide": "\"Tide\" returns the day's high and low tides",\
             "sun": "\"Sun\" returns the day's sunrise and sunset",\
             "goog": "\"Goog Seattle Central Library Hours\" returns scraped \"smart\" answer from search engine. Hopefully relevant.",\
             "cal": "Use following comma sep format to add: \"Cal, hg, 10/5 9a\". To check specific date: \"cal 6/5\"",\
             "map": "Enter:\"m, origin, dest, mode.\" eg: \"m, 110 vine st seattle wa, fremont brewing company seattle wa, transit",\
             "limebike": "Enter: \"limebike bikenumber. No other spaces or funny business\" eg: \"lime 123456\". Just those two!"}

def helperfunc(text):
    if text[:1] == "1" or text[:1]=="w":
        res = help_dict["weather"]
    elif text[:1]=="2" or text[:3]=="cal":
        res = help_dict["cal"]
    elif text[:1]=="3" or text=="m" or text[:3]=="map":
        res = help_dict["map"]
    elif text[:1]=="4" or text[:4]=="lime" or text[:4]=="bike" or text[:4]=="spin":
        res = help_dict["limebike"]
    elif text[:1]=="5" or text == "cab" or text=="chariot" or text=="taxi":
        res = help_dict["chariot"]
    elif text[:1]=="6" or text=="tides" or text=="tide" or text=="t":
        res = help_dict["tide"]
    elif text[:1]=="7" or text[:3]=="sun":
        res = help_dict["sun"]
    elif text[:1]=="8" or text[:4]=="goog" or text == "bing":
        res = help_dict["goog"]
    else:
        res = "\"help function-name\" gives help for that function! eg: \"help sun\" "
    return res