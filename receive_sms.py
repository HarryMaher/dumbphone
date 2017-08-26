#!/usr/bin/env python3

'''
Receive SMS

This takes in text messages (SMS) sent to a specific Twilio number
and replies with the response determined by dumbphone.py

Note: this won't send a reply for the Limebike function because that function takes more than
15 seconds to complete so the server times out - instead it sends a message to the phone notifying
whether it worked or the bike is broken or whatever
requires:
python3
flask
twilio
'''

from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from dumbphone import DumbphoneResponse


app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    # """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)

    # Check if incoming text is from my phone number...

    # Start our TwiML response
    resp = MessagingResponse()
    # Response generated by dumbphone.py with Dumbphone_Response class
    msg_response = DumbphoneResponse(body)
    text_this = msg_response.dumbphone_responder()
    resp.message(text_this)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)

