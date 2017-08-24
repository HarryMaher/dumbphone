#!/usr/bin/python

'''
NOTE BEFORE UPLOADING TO GITHUB:
Save SID and token in files with .gitignore and return the others.
And phone numbers!!
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