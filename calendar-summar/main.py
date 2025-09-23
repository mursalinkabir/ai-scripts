import os
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# --- Google Calendar API Configuration ---
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.json'

# --- Slack API Configuration ---
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_CHANNEL = "#general"  # Change this to your desired channel

def get_calendar_events():
    """
    Connects to the Google Calendar API and fetches tomorrow's events.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    time_min = datetime.datetime.combine(tomorrow, datetime.time.min).isoformat() + 'Z'
    time_max = datetime.datetime.combine(tomorrow, datetime.time.max).isoformat() + 'Z'

    events_result = service.events().list(calendarId='primary', timeMin=time_min,
                                        timeMax=time_max, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    return events

def post_to_slack(events):
    """
    Posts a summary of the given events to a Slack channel.
    """
    if not SLACK_BOT_TOKEN:
        print("Error: SLACK_BOT_TOKEN environment variable not set.")
        return

    client = WebClient(token=SLACK_BOT_TOKEN)

    if not events:
        message = "No upcoming events for tomorrow."
    else:
        message = "Upcoming events for tomorrow:\n"
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            message += f"- {start} {event['summary']}\n"

    try:
        response = client.chat_postMessage(
            channel=SLACK_CHANNEL,
            text=message
        )
        print(f"Message posted to {SLACK_CHANNEL}")
    except SlackApiError as e:
        print(f"Error posting to Slack: {e.response['error']}")

def main():
    """
    Main function to get calendar events and post them to Slack.
    """
    events = get_calendar_events()
    post_to_slack(events)

if __name__ == '__main__':
    main()
