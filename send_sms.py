#!/usr/bin/python

'''
Sends an SMS using twilio. You must sign up for twilio and have your sid stored in twilio_sid.txt
and an auth token in twilio_auth_token.txt. Store your twilio phone number in twilio_number.txt
and your phone number in my_cell_number.txt

'''

import os
from twilio.rest import Client

file = open("twilio_sid.txt")
account_sid = file.read()
file.close()

file = open("twilio_auth_token.txt")
auth_token = file.read()
file.close()

file = open("twilio_number.txt")
from_number = file.read()
file.close()

file = open("my_cell_number.txt")
to_number = file.read()
file.close()

client = Client(account_sid, auth_token)

def send_message(message_content):
	client.messages.create(
	to=to_number,
	from_=from_number,
	body=message_content
	)