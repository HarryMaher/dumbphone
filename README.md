# dumbphone #


### *Harry Maher* ###

A final project for my intro to python class. 
dumbphone--*it makes your dumb phone smart!*

## *Description* ##

A Python program that runs (ideally on a server 24/7) for you to text for information
that you otherwise only get with a smart phone & data plan. I currently have this running on a raspberry pi.
It uses Twilio to send/receive messages, and dumbphone.py to handle incoming texts.

For educational purposes only!


## Why: ##
- Smartphones = worst & I recently gave mine up
  - Current apps are designed to catch & keep our attention to deliver useless "content"
  - Too much screen time bad for mental health, memory, happiness
  - I made an attempt at writing a program to that performs some useful ("smart") functions but won't addict users

### Instructions ###

Clone this repo:
```
$ git clone https://github.com/HarryMaher/dumbphone
```

## Set up: ##
- Follow Twilio starter instructions below
- Install all dependencies listed in dumbphone.py
- Run receive_sms.py
- run ngrok (the windows .exe is in this directory, but otherwise - https://ngrok.com/download)
- Follow more Twilio instructions (same video below)
- Read the docstrings for each of these smaller programs and web search extensively to get the rest of it working
- Contact me with further issues


Read the docstrings for each of the functions if you want full functionality.
The first three functions require that you get your own API keys,
and the fourth requires that you have an android emulator running on your computer

Current functions include:
1. *Weather* –  forecasts & current conditions (Wunderground API)
2. *Maps* – text-based directions (Google Maps API)
3. *Calendar* – view and add events (Calendar API)
4. *Limebike* – text bike number – android emulator does the rest (pyautogui)
5. *Chariot* – returns phone numbers for big city cab companies (a la Lyft)
6. *Tides* – tides of day (For less soggy beach naps)
7. *Sun* – what time it’ll set/rise ("Shabattify" - Dan O.)
8. *Goog* – “Smart answers” from a *search engine*. Scrapes the smart box answers.

--------- 
### Twilio Starter ###

Set up an account and [follow these instructions](https://www.youtube.com/watch?v=cZeCz_QOoXw). 

---------

Contact me with any questions!