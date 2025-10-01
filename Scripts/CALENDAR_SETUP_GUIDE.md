# Google Calendar Integration Setup Guide

This guide will help you set up automatic calendar events for job application deadlines.

---

## 🎯 What This Does

- **Automatically creates Google Calendar events** for every job deadline
- **Works on ALL devices** (PC, Mac, phone, web)
- **Smart reminders** based on urgency:
  - 🚨 URGENT: Reminders at 1 day, 12 hours, 2 hours before
  - ⏰ HIGH PRIORITY: Reminders at 3 days, 1 day before
  - 📅 MODERATE: Reminders at 1 week, 3 days before
- **Color-coded events** (Red for urgent, Yellow for high priority, etc.)
- **Works even when chat is closed**

---

## 📋 One-Time Setup (15 minutes)

### Step 1: Enable Google Calendar API

1. Go to: https://console.cloud.google.com/
2. Click **"Select a project"** → **"New Project"**
3. Project name: `Job Application Tracker`
4. Click **"Create"**
5. Wait for project to be created (30 seconds)

### Step 2: Enable Calendar API

1. In the search bar, type: `Calendar API`
2. Click **"Google Calendar API"**
3. Click **"Enable"**
4. Wait for API to be enabled

### Step 3: Create OAuth Credentials

1. Click **"Create Credentials"** (top right)
2. Select:
   - **Which API are you using?** → Google Calendar API
   - **What data will you be accessing?** → User data
3. Click **"Next"**
4. Fill in OAuth consent screen:
   - **App name:** Job Application Tracker
   - **User support email:** obai@obaisukar.com
   - **Developer contact:** obai@obaisukar.com
5. Click **"Save and Continue"**
6. **Scopes:** Click "Add or Remove Scopes"
   - Search for: `calendar`
   - Check: `https://www.googleapis.com/auth/calendar`
   - Click **"Update"**
7. Click **"Save and Continue"**
8. **OAuth Client ID:**
   - Application type: **Desktop app**
   - Name: Job Application Tracker
9. Click **"Create"**

### Step 4: Download Credentials

1. Click **"Download"** button (⬇️ icon)
2. This downloads `client_secret_....json`
3. **Rename file to:** `credentials.json`
4. **Move to:** `/Volumes/Raid/Claude/Applications/job-applications/Scripts/credentials.json`

### Step 5: Install Python Dependencies

```bash
pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### Step 6: Run Calendar Sync

```bash
cd /Volumes/Raid/Claude/Applications/job-applications/Scripts
python3 calendar_integration.py
```

**What happens:**
1. Browser opens asking for Google sign-in
2. Sign in with your Google account
3. Click **"Allow"** to give calendar access
4. Script creates calendar events for all deadlines
5. ✅ Done! Check your Google Calendar

---

## 🔄 Usage

### Sync Deadlines Anytime

```bash
cd /Volumes/Raid/Claude/Applications/job-applications/Scripts
python3 calendar_integration.py
```

### Automatic Sync (Optional)

Add to cron/LaunchAgent to run daily:

```bash
# Run at 9 AM daily
0 9 * * * cd /Volumes/Raid/Claude/Applications/job-applications/Scripts && python3 calendar_integration.py
```

### When Claude Adds New Jobs

After I add a new job with a deadline, you can either:
1. **Manual:** Run `python3 calendar_integration.py`
2. **Automatic:** Set up daily sync (see above)
3. **Ask me:** Just say "sync calendar" and I'll run it for you

---

## 🎨 Calendar Event Details

### Event Title Format
```
🎯 Job Application Due: [Company Name - Position]
```

### Event Description Includes
- Position title
- Application method (LinkedIn, email, Google Form, etc.)
- Urgency level
- Folder path
- Direct link to tracker file

### Color Coding
- 🔴 **Red:** URGENT deadlines (apply today/tomorrow)
- 🟡 **Yellow:** HIGH PRIORITY (3-7 days)
- 🔵 **Cyan:** MODERATE (1-2 weeks)
- ⚪ **Gray:** FLEXIBLE (no specific deadline)

### Reminder Schedule

**🚨 URGENT:**
- 1 day before (popup + email)
- 12 hours before (popup)
- 2 hours before (popup)

**⏰ HIGH PRIORITY:**
- 3 days before (popup + email)
- 1 day before (popup)

**📅 MODERATE:**
- 1 week before (popup + email)
- 3 days before (popup)

**⏳ FLEXIBLE:**
- 1 week before (popup)

---

## 🔧 Troubleshooting

### "credentials.json not found"
- Make sure you downloaded OAuth credentials from Google Cloud Console
- Rename to exactly `credentials.json`
- Place in `/Volumes/Raid/Claude/Applications/job-applications/Scripts/`

### "Authentication failed"
- Delete `.calendar_token.pickle` and re-run script
- Browser will open for re-authentication

### "No module named google"
- Run: `pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`

### Events not appearing in calendar
- Check you're signed into the correct Google account
- View "primary" calendar (not a secondary calendar)
- Refresh Google Calendar page

### Multiple duplicate events
- Script creates events each time it runs
- Manually delete duplicates in Google Calendar
- Future version will check for existing events

---

## 🔐 Security Notes

- **credentials.json** contains OAuth client ID (not sensitive, but keep private)
- **.calendar_token.pickle** contains your auth token (DO NOT share or commit to git)
- Both files are in `.gitignore` for safety
- You can revoke access anytime at: https://myaccount.google.com/permissions

---

## 📱 Access Your Calendar

- **Web:** https://calendar.google.com
- **iPhone:** Google Calendar app
- **Android:** Google Calendar app (pre-installed)
- **Windows:** Add Google Calendar to Outlook
- **Mac:** Add Google account to Apple Calendar

---

## ✨ Benefits

✅ Never miss a deadline
✅ Works across all devices
✅ No manual checking needed
✅ Smart reminders based on urgency
✅ Visual color coding
✅ Works when chat is closed
✅ Works on PC, Mac, and phone

---

**Need help?** Just ask Claude in chat: "help with calendar setup"

**Last Updated:** October 1, 2025
