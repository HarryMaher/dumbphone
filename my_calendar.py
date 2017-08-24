#!/usr/bin/env python3

'''

Calendar function - given date prints next few events. Default prints next upcoming events
with "cal 8/23" prints next events on that date
"cal, work, 10/5 9am" adds "work to that date and time...

To Do:
- delete events option? (sounds dangerous though so maybe not)
- take end time for events. but that's low priority for now


This function is heavily borrowed from one written by engineers at Google
for their calendar api quickstart for python.
To get started with this API, see instructions here:
https://developers.google.com/google-apps/calendar/quickstart/python

Also, if you don't live in the west coast (why?) of US, change the time zone
information including from the -7 hours at the end to whatever your UTC requirements are...


requires
httplib2
oauth2client
apiclient
python3

'''

from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime


current_year = datetime.datetime.now().strftime("%Y")

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential. Note- is stored in Users/User/.credentials folder
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        print('Storing credentials to ' + credential_path)
    return credentials

# rewrote the main function to take an input string... it's kinda complicated but here goes
# an input of "cal" just gives the next 2 events
# "cal 7/12" would give the first 2 events of that day.
# "cal, hg 9-2, 6/12 9a" puts an event in the calendar called "hg 9-2"
def main(input_string):
    try:
        if len(input_string.split(" "))==2:
            if input_string.split(" ")[1]== "help":
                return "use following comma sep format to add: \"Cal, hg, 10/5 9a\". To check specific date: \"cal 6/5\""
        if len(input_string.split(",")) > 2:
            add_event(input_string)
            return "event added!"
        else:
            """
            Creates a Google Calendar API service object and outputs a list of either next 4 events on the calendar,
            or next 4 events on specified date and returns the first 140 chars of those event titles, times, and dates.
            """
            credentials = get_credentials()
            http = credentials.authorize(httplib2.Http())
            service = discovery.build('calendar', 'v3', http=http)

            now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

            if len(input_string.split(" ")) ==  2:
                start_date = input_string.split(" ")[1]
                start_date = start_date.replace("/", "-")
                start_date_list = start_date.split("-")
                start_date_list[0] = start_date_list[0].rjust(2, "0")
                start_date_list[1] = start_date_list[1].rjust(2, "0")
                start_date = "-".join(start_date_list)
                now = current_year+'-'+start_date+'T00:00:00-07:00'

            eventsResult = service.events().list(
                calendarId='primary', timeMin=now, maxResults=4, singleEvents=True,
                orderBy='startTime').execute()
            events = eventsResult.get('items', [])
            if not events:
                return 'No upcoming events found.'
            all_events_string = ""
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))[5:]
                if len(start) > 10:
                    start= start[:5]+" "+start[6:11]
                all_events_string +=  "{} {}.\n".format(start, event['summary'])
            all_events_string = str(all_events_string)[:140]
            return all_events_string
    except:
        return "error - use following comma separated format to add: \"Cal, hg, 10/5 9a\" or see date: \"cal 6/7\""



# input is a string separated by commas with "calendar, event name, start datetime(MM-DD time), optional end datetime.
# Default to an hour past start datetime.
# Note space in second argument.
# optional
def add_event(input_string):
    input_list = input_string.split(",")
    summary = input_list[1].strip()
    start_date = input_list[2].strip().split(" ")[0]
    start_date = start_date.replace("/","-")
    start_date_list = start_date.split("-")
    start_date_list[0] = start_date_list[0].rjust(2,"0")
    start_date_list[1] = start_date_list[1].rjust(2,"0")
    start_date = "-".join(start_date_list)
    start_time = input_list[2].strip().split(" ")[1]
    if "p" in start_time:
        start_time = start_time.replace("pm", "")
        start_time = start_time.replace("p", "")
        start_time_list = start_time.split(":")
        # this may be lazy, but works for now... Adds 12 to the time if pm!
        try:
            start_time = str(int(start_time_list[0])+12).rjust(2,"0")+":"+start_time_list[1]
        except:
            start_time = str(int(start_time_list[0])+12)
    elif "a" in start_time:
        start_time = start_time.replace("am","")
        start_time = start_time.replace("a","")
    if ":" in start_time:
        start_date_time = current_year+'-'+start_date+'T'+start_time+':00-07:00'
        end_date_time = current_year + '-'+start_date+'T'+start_time+':00-07:00'
    else:
        start_time = start_time.rjust(2, "0")
        start_date_time = current_year+'-'+start_date+'T'+start_time+':00:00-07:00'
        end_date_time = current_year+'-'+start_date+'T'+start_time+':00:00-07:00'
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    event = {
        'summary': summary,
        'description': summary,
        'start': {
            'dateTime': start_date_time,
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': end_date_time,
            'timeZone': 'America/Los_Angeles',
        }
    }
    event = service.events().insert(calendarId='primary', body=event).execute()
    return ('Event created: {}'.format(event.get('htmlLink')))