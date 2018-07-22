"""
Most of this code is from Google: https://developers.google.com/calendar/quickstart/python
Shows basic usage of the Google Calendar API. Creates a Google Calendar API
service object and outputs a list of the next 10 events on the user's calendar.
"""
from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime

# to store the day (which incorrect because the box I'm doing it on is in a different timezone via pythonanywhere)
now = datetime.datetime.now()
day = int(now.day)

# Setup the Calendar API
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
store = file.Storage('token.json')
creds = store.get()
if not creds or creds.invalid:
# if you have the credentials in the same directory (generated via https://developers.google.com/calendar/quickstart/python)
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('calendar', 'v3', http=creds.authorize(Http()))

# Call the Calendar API
# this grabs only events from the time of grabbing onward. I can solve this by
# having the program run early in the morning... Then I can schedule the email to send or just have it send in the morning and get to it at night
now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
events_result = service.events().list(calendarId='primary', timeMin=now,
                                      maxResults=10, singleEvents=True,
                                      orderBy='startTime').execute()
events = events_result.get('items', [])

list_of_events = ''

if not events:
    print('No upcoming events found.')
for event in events:
    print(day-1)
    if (day) == int(event['start']['dateTime'][8:10]):
        start = event['start'].get('dateTime', event['start'].get('date'))
        list_of_events += "\nEvent Title: " + event['summary']
# Stores all the events in a list that is sent via email

## All the code above gets me all the events for a day.

# Now I want to push this event info to a spreadsheet.

# Ok I am actually going to wait on this. For the moment I just want to immiate Sunsama's daily update...
# I can move that to a Google form then... I can just have a bunch of entries for events on the Form then go from there

# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import sendgrid
import os
from sendgrid.helpers.mail import *

# check out the sendgrid api docs for information about how to get the apikey
sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
from_email = Email("test@example.com")
to_email = Email("YOUR EMAIL")
subject = "Daily Routine Check In"
content = Content("text/plain", list_of_events + '\nhttps://docs.google.com/forms/d/e/1FAIpQLSdV0RmRZyGzmhMnQ5nL_EQWK54dYGcbXUvyJ02m0AHyl1CAWA/viewform?usp=sf_link')
mail = Mail(from_email, subject, to_email, content)
response = sg.client.mail.send.post(request_body=mail.get())
# prints info from successful email
print(response.status_code)
print(response.body)
print(response.headers)

