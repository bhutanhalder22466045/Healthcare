import os
import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Path to the credentials file
CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), "credentials.json")

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def get_calendar_service():
    """Authenticate and return the Google Calendar service object."""
    creds = service_account.Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
    service = build("calendar", "v3", credentials=creds)
    return service

def create_calendar_event(doctor_name, appointment_date, start_time):
    """Creates a Google Calendar event for the appointment."""
    service = get_calendar_service()

    start_datetime = datetime.datetime.combine(appointment_date, start_time)
    end_datetime = start_datetime + datetime.timedelta(minutes=45)

    event = {
        "summary": f"Appointment with Dr. {doctor_name}",
        "description": "Doctor Appointment Scheduled via Django App",
        "start": {"dateTime": start_datetime.isoformat(), "timeZone": "UTC"},
        "end": {"dateTime": end_datetime.isoformat(), "timeZone": "UTC"},
    }

    event = service.events().insert(calendarId="primary", body=event).execute()
    return event.get("htmlLink")  # Returns Google Calendar event link
