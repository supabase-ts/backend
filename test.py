from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        event = {
          'summary': 'Financial Advisor Meet',
          'description': 'A chance to hear more about Google\'s developer products.',
          'start': {
            'dateTime': '2023-07-30T15:00:00+07:00',
            'timeZone': 'Asia/Jakarta',
          },
          'end': {
            'dateTime': '2023-07-30T16:00:00+07:00',
            'timeZone': 'Asia/Jakarta',
          },
          'attendees': [
            {'email': 'arkan.alexei@ui.ac.id'}
          ],
          'reminders': {
            'useDefault': False,
            'overrides': [
              {'method': 'email', 'minutes': 24 * 60},
              {'method': 'popup', 'minutes': 10},
            ],
          },
            'conferenceData': {
                'createRequest': {
                    'requestId': 'sample123',  # You can generate this randomly
                    'conferenceSolutionKey': {
                        'type': 'hangoutsMeet'
                    },
                },
            },

        }
        event = service.events().insert(calendarId='primary', conferenceDataVersion=1, body=event).execute()
        print('Event created: %s' % (event.get('htmlLink')))
        print('Google Meet Link: %s' % (event['conferenceData']['entryPoints'][0]['uri']))

    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()
