import datetime
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from django.conf import settings

SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = settings.GOOGLE_CREDENTIALS_FILE


def create_google_calendar_event(appointment):
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )

    service = build('calendar', 'v3', credentials=credentials)

    start_time = datetime.datetime.combine(appointment.date, appointment.start_time)
    end_time = datetime.datetime.combine(appointment.date, appointment.end_time)

    event = {
        'summary': f'Appointment with Dr. {appointment.doctor.first_name} {appointment.doctor.last_name}',
        'start': {'dateTime': start_time.isoformat(), 'timeZone': 'UTC'},
        'end': {'dateTime': end_time.isoformat(), 'timeZone': 'UTC'},
        'attendees': [{'email': appointment.doctor.email}, {'email': appointment.patient.email}],
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    return event['id']
