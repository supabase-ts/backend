from datetime import timedelta, datetime
import os.path

import requests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from user.models import User, Advisor, Appointment


class AppointmentAPIView(GenericAPIView):
    def post(self, request):
        customer_account_no = request.data.get('customerAccountNo')
        advisor_account_no = request.data.get('advisorAccountNo')
        start_time = request.data.get('start_time')
        token = request.data.get('token')

        customer = User.objects.filter(account_no=customer_account_no).first()
        advisor = Advisor.objects.filter(user__account_no=advisor_account_no).first()
        price = advisor.rate_per_hour

        # Perform transaction
        transaction_url = 'http://34.101.154.14:8175/hackathon/bankAccount/transaction/create'
        transaction_data = {
            "senderAccountNo": customer.account_no,
            "receiverAccountNo": advisor.user.account_no,
            "amount": price
        }
        headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
        response = requests.post(transaction_url, headers=headers, json=transaction_data)
        if response.status_code != 200:
            return Response({"error": "Transaction failed"}, status=status.HTTP_400_BAD_REQUEST)

        # Create Google Meet event
        meet_url = self.create_meet_event(customer.email, advisor.user.email, start_time)
        if not meet_url:
            return Response({"error": "Failed to create Google Meet event"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Create appointment
        appointment = Appointment.objects.create(
            customer=customer, advisor=advisor, meet_url=meet_url, start_time=start_time
        )

        return Response({"success": f"Appointment created with id {appointment.id}"},
                        status=status.HTTP_201_CREATED)

    def create_meet_event(self, customer_email, advisor_email, start_time):
        SCOPES = ['https://www.googleapis.com/auth/calendar']

        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        try:
            service = build('calendar', 'v3', credentials=creds)
            start_time_str = self.start_to_gmt_7(start_time)
            end_time_str = self.add_one_hour(start_time)

            print("Start time:", start_time_str)
            print("End time:", end_time_str)
            event = {
                'summary': 'Financial Advisor Meet',
                'description': 'A chance to hear more about Google\'s developer products.',
                'start': {
                    'dateTime': start_time_str,
                    'timeZone': 'Asia/Jakarta',
                },
                'end': {
                    'dateTime': end_time_str,
                    'timeZone': 'Asia/Jakarta',
                },
                'attendees': [
                    {'email': customer_email},
                    {'email': advisor_email}
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
            meet_url = event['conferenceData']['entryPoints'][0]['uri']
            return meet_url

        except HttpError:
            return None

    def start_to_gmt_7(self, start_time_str):
        start_time = datetime.fromisoformat(start_time_str.replace("Z", "+07:00"))
        return start_time.isoformat(timespec='seconds')

    def add_one_hour(self, start_time_str):
        start_time = datetime.fromisoformat(start_time_str.replace("Z", "+07:00"))
        end_time = start_time + timedelta(hours=1)
        return end_time.isoformat(timespec='seconds')
