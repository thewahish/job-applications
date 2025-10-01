#!/usr/bin/env python3
"""
Job Application Deadline Calendar Integration
Automatically creates Google Calendar events for job application deadlines
"""

import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    import pickle
except ImportError:
    print("❌ Required packages not installed.")
    print("📦 Installing dependencies...")
    os.system('pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib')
    print("✅ Dependencies installed. Please run the script again.")
    sys.exit(1)

# Configuration
SCOPES = ['https://www.googleapis.com/auth/calendar']
TRACKER_FILE = '/Volumes/Raid/Claude/Applications/job-applications/Jobs/SPECIAL_REQUIREMENTS_TRACKER.md'
TOKEN_FILE = '/Volumes/Raid/Claude/Applications/job-applications/Scripts/.calendar_token.pickle'
CREDENTIALS_FILE = '/Volumes/Raid/Claude/Applications/job-applications/Scripts/credentials.json'

class CalendarIntegration:
    def __init__(self):
        self.creds = None
        self.service = None

    def authenticate(self):
        """Authenticate with Google Calendar API"""
        # Load existing credentials
        if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE, 'rb') as token:
                self.creds = pickle.load(token)

        # If credentials don't exist or are invalid, get new ones
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                if not os.path.exists(CREDENTIALS_FILE):
                    print("❌ credentials.json not found!")
                    print("\n📋 SETUP INSTRUCTIONS:")
                    print("1. Go to: https://console.cloud.google.com/")
                    print("2. Create a new project (or select existing)")
                    print("3. Enable Google Calendar API")
                    print("4. Create OAuth 2.0 credentials (Desktop app)")
                    print("5. Download credentials.json")
                    print(f"6. Save to: {CREDENTIALS_FILE}")
                    print("\nThen run this script again.")
                    sys.exit(1)

                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_FILE, SCOPES)
                self.creds = flow.run_local_server(port=0)

            # Save credentials for next run
            with open(TOKEN_FILE, 'wb') as token:
                pickle.dump(self.creds, token)

        self.service = build('calendar', 'v3', credentials=self.creds)
        print("✅ Authenticated with Google Calendar")

    def parse_deadline(self, deadline_str):
        """Parse deadline string to extract date and urgency"""
        # Look for date patterns like "October 2, 2025" or "2025-10-02"
        date_patterns = [
            r'(\w+ \d{1,2}, \d{4})',  # October 2, 2025
            r'(\d{4}-\d{2}-\d{2})',    # 2025-10-02
        ]

        for pattern in date_patterns:
            match = re.search(pattern, deadline_str)
            if match:
                date_str = match.group(1)
                try:
                    # Try parsing different formats
                    for fmt in ['%B %d, %Y', '%Y-%m-%d']:
                        try:
                            deadline_date = datetime.strptime(date_str, fmt)

                            # Determine urgency
                            if '🚨' in deadline_str:
                                urgency = 'URGENT'
                            elif '⏰' in deadline_str:
                                urgency = 'HIGH_PRIORITY'
                            elif '📅' in deadline_str:
                                urgency = 'MODERATE'
                            else:
                                urgency = 'FLEXIBLE'

                            return deadline_date, urgency
                        except ValueError:
                            continue
                except Exception as e:
                    continue

        return None, None

    def extract_jobs_from_tracker(self):
        """Extract job information from SPECIAL_REQUIREMENTS_TRACKER.md"""
        jobs = []
        current_job = {}

        with open(TRACKER_FILE, 'r') as f:
            for line in f:
                line = line.strip()

                # Job title
                if line.startswith('### ') and not line.startswith('### When'):
                    if current_job and 'title' in current_job:
                        jobs.append(current_job)
                    current_job = {'title': line.replace('### ', '')}

                # Deadline
                elif '**Application Deadline:**' in line:
                    deadline_str = line.split('**Application Deadline:**')[1].strip()
                    deadline_date, urgency = self.parse_deadline(deadline_str)
                    if deadline_date:
                        current_job['deadline'] = deadline_date
                        current_job['urgency'] = urgency
                        current_job['deadline_str'] = deadline_str

                # Folder path
                elif '**Folder:**' in line:
                    folder = line.split('**Folder:**')[1].strip().replace('`', '')
                    current_job['folder'] = folder

                # Application method
                elif '**Application Method:**' in line:
                    method = line.split('**Application Method:**')[1].strip()
                    current_job['method'] = method

        # Add last job
        if current_job and 'title' in current_job:
            jobs.append(current_job)

        return jobs

    def create_calendar_event(self, job):
        """Create a Google Calendar event for a job deadline"""
        if 'deadline' not in job:
            return None

        deadline = job['deadline']
        title = job['title']
        urgency = job.get('urgency', 'FLEXIBLE')
        method = job.get('method', 'Standard')
        folder = job.get('folder', 'N/A')

        # Event details
        summary = f"🎯 Job Application Due: {title}"
        description = f"""Job Application Deadline

Position: {title}
Application Method: {method}
Urgency: {urgency}
Deadline: {job.get('deadline_str', 'See calendar')}

Folder: {folder}

📋 Tracker: {TRACKER_FILE}

⚡ Action Required: Complete and submit application materials
"""

        # Set event time to 9 AM on deadline day
        start_datetime = deadline.replace(hour=9, minute=0, second=0)
        end_datetime = start_datetime + timedelta(hours=1)

        event = {
            'summary': summary,
            'description': description,
            'start': {
                'dateTime': start_datetime.isoformat(),
                'timeZone': 'America/Detroit',
            },
            'end': {
                'dateTime': end_datetime.isoformat(),
                'timeZone': 'America/Detroit',
            },
            'reminders': {
                'useDefault': False,
                'overrides': self.get_reminders(urgency, deadline),
            },
            'colorId': self.get_color_id(urgency),
        }

        try:
            event = self.service.events().insert(calendarId='primary', body=event).execute()
            print(f"✅ Created event: {title} ({urgency}) - {deadline.strftime('%Y-%m-%d')}")
            return event
        except Exception as e:
            print(f"❌ Error creating event for {title}: {e}")
            return None

    def get_reminders(self, urgency, deadline):
        """Get reminder settings based on urgency"""
        reminders = []

        if urgency == 'URGENT':
            # More frequent reminders for urgent deadlines
            reminders = [
                {'method': 'popup', 'minutes': 24 * 60},  # 1 day before
                {'method': 'popup', 'minutes': 12 * 60},  # 12 hours before
                {'method': 'popup', 'minutes': 2 * 60},   # 2 hours before
                {'method': 'email', 'minutes': 24 * 60},  # Email 1 day before
            ]
        elif urgency == 'HIGH_PRIORITY':
            reminders = [
                {'method': 'popup', 'minutes': 3 * 24 * 60},  # 3 days before
                {'method': 'popup', 'minutes': 24 * 60},      # 1 day before
                {'method': 'email', 'minutes': 3 * 24 * 60},  # Email 3 days before
            ]
        elif urgency == 'MODERATE':
            reminders = [
                {'method': 'popup', 'minutes': 7 * 24 * 60},  # 1 week before
                {'method': 'popup', 'minutes': 3 * 24 * 60},  # 3 days before
                {'method': 'email', 'minutes': 7 * 24 * 60},  # Email 1 week before
            ]
        else:  # FLEXIBLE
            reminders = [
                {'method': 'popup', 'minutes': 7 * 24 * 60},  # 1 week before
            ]

        return reminders

    def get_color_id(self, urgency):
        """Get calendar color based on urgency"""
        # Google Calendar color IDs
        colors = {
            'URGENT': '11',        # Red
            'HIGH_PRIORITY': '5',  # Yellow
            'MODERATE': '7',       # Cyan
            'FLEXIBLE': '8',       # Gray
        }
        return colors.get(urgency, '8')

    def sync_deadlines(self):
        """Sync all deadlines from tracker to Google Calendar"""
        print("📅 Syncing job application deadlines to Google Calendar...\n")

        jobs = self.extract_jobs_from_tracker()
        print(f"📋 Found {len(jobs)} jobs in tracker")

        jobs_with_deadlines = [j for j in jobs if 'deadline' in j]
        print(f"📅 {len(jobs_with_deadlines)} jobs have deadlines\n")

        created_count = 0
        for job in jobs_with_deadlines:
            event = self.create_calendar_event(job)
            if event:
                created_count += 1

        print(f"\n✅ Successfully created {created_count} calendar events!")
        print(f"📱 Check your Google Calendar for reminders")

def main():
    print("🚀 Job Application Deadline Calendar Integration\n")

    if not os.path.exists(TRACKER_FILE):
        print(f"❌ Tracker file not found: {TRACKER_FILE}")
        sys.exit(1)

    calendar = CalendarIntegration()
    calendar.authenticate()
    calendar.sync_deadlines()

if __name__ == '__main__':
    main()
