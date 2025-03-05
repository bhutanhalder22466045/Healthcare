from datetime import datetime, timedelta
from utils import get_calendar_service

service = get_calendar_service()

event = {
    'summary': 'Test Appointment',
    'description': 'This is a test event from Django',
    'start': {'dateTime': datetime.utcnow().isoformat(), 'timeZone': 'UTC'},
    'end': {'dateTime': (datetime.utcnow() + timedelta(minutes=45)).isoformat(), 'timeZone': 'UTC'},
}

event = service.events().insert(calendarId='primary', body=event).execute()
print('Event created:', event.get('htmlLink'))
