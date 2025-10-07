# Google Calendar Integration - Complete Setup Guide

**Status:** Ready for setup (pending user action)
**Last Updated:** October 1, 2025

---

## 📋 Overview

This document contains everything you need to set up automated Google Calendar notifications for job application deadlines.

**What this does:**
- ✅ Automatically creates calendar events for every job deadline
- ✅ Works on ALL devices (PC, Mac, phone, web)
- ✅ Works even when Claude chat is closed
- ✅ Smart reminders based on urgency
- ✅ Color-coded events (Red=Urgent, Yellow=High Priority, etc.)

**Time required:** ~15 minutes (one-time setup)

---

## 🚀 Quick Start (Step-by-Step)

### **Step 1: Set up Google Cloud Project**

1. Go to: **https://console.cloud.google.com/**
2. Sign in with your Google account (obai@obaisukar.com)
3. Click **"Select a project"** dropdown (top left)
4. Click **"NEW PROJECT"** button
5. Fill in:
   - **Project name:** `Job Application Tracker`
   - **Location:** Leave as default (No organization)
6. Click **"CREATE"**
7. Wait ~30 seconds for project creation

### **Step 2: Enable Google Calendar API**

1. Once project is created, use the **search bar at top**
2. Type: `Calendar API`
3. Click **"Google Calendar API"** from results
4. Click the blue **"ENABLE"** button
5. Wait for API to enable (~10 seconds)

### **Step 3: Configure OAuth Consent Screen**

1. In the left sidebar, click **"OAuth consent screen"**
2. Select **"External"** user type
3. Click **"CREATE"**
4. Fill in required fields:
   - **App name:** `Job Application Tracker`
   - **User support email:** `obai@obaisukar.com`
   - **Developer contact information:** `obai@obaisukar.com`
5. Click **"SAVE AND CONTINUE"**

### **Step 4: Add Calendar Scope**

1. On the "Scopes" page, click **"ADD OR REMOVE SCOPES"**
2. In the filter box, type: `calendar`
3. Check the box for: `https://www.googleapis.com/auth/calendar`
4. Click **"UPDATE"**
5. Click **"SAVE AND CONTINUE"**

### **Step 5: Add Test Users**

1. On "Test users" page, click **"ADD USERS"**
2. Enter: `obai@obaisukar.com`
3. Click **"ADD"**
4. Click **"SAVE AND CONTINUE"**

### **Step 6: Create OAuth Credentials**

1. In left sidebar, click **"Credentials"**
2. Click **"+ CREATE CREDENTIALS"** (top)
3. Select **"OAuth client ID"**
4. Configure:
   - **Application type:** Desktop app
   - **Name:** `Job Application Tracker Desktop`
5. Click **"CREATE"**
6. You'll see "OAuth client created" dialog

### **Step 7: Download Credentials**

1. Click **"DOWNLOAD JSON"** button (or ⬇️ download icon)
2. This downloads a file like: `client_secret_XXXXX.json`
3. **Rename the file to exactly:** `credentials.json`
4. **Move it to:** `/Volumes/Raid/Claude/Applications/job-applications/Scripts/credentials.json`

### **Step 8: Install Python Dependencies**

Open Terminal and run:

```bash
pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

If you don't have pip3 installed:

```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3
brew install python3

# Then install dependencies
pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### **Step 9: Run Calendar Integration**

```bash
cd /Volumes/Raid/Claude/Applications/job-applications/Scripts
python3 calendar_integration.py
```

**What happens:**
1. Your browser will automatically open
2. Google will ask you to sign in (use obai@obaisukar.com)
3. You'll see a warning "Google hasn't verified this app" - Click **"Advanced"** → **"Go to Job Application Tracker (unsafe)"**
4. Click **"Allow"** to give calendar access
5. Browser shows "The authentication flow has completed"
6. Script creates calendar events for all deadlines
7. ✅ Done!

### **Step 10: Verify in Google Calendar**

1. Go to: **https://calendar.google.com**
2. You should see new events like: "🎯 Job Application Due: [Company Name]"
3. Check that reminders are set correctly
4. Events are color-coded by urgency

---

## 🎨 Calendar Event Features

### Event Format

**Title:** `🎯 Job Application Due: [Company - Position]`

**Description includes:**
- Position title
- Application method (LinkedIn, email, Google Form)
- Urgency level
- Folder path in your job tracker
- Link to SPECIAL_REQUIREMENTS_TRACKER.md

### Color Coding

- 🔴 **Red (#11):** URGENT (apply today/tomorrow)
- 🟡 **Yellow (#5):** HIGH PRIORITY (3-7 days)
- 🔵 **Cyan (#7):** MODERATE (1-2 weeks)
- ⚪ **Gray (#8):** FLEXIBLE (no specific deadline)

### Smart Reminders

**🚨 URGENT Deadlines:**
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

## 🔄 Daily Usage

### When Claude Adds a New Job with Deadline

**Option 1: Ask Claude to sync**
```
Just say in chat: "sync calendar"
```

**Option 2: Run manually**
```bash
cd /Volumes/Raid/Claude/Applications/job-applications/Scripts
python3 calendar_integration.py
```

**Option 3: Set up automatic daily sync (optional)**

Create a LaunchAgent to run daily at 9 AM:

```bash
cat > ~/Library/LaunchAgents/com.obaisukar.calendarsync.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.obaisukar.calendarsync</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/python3</string>
        <string>/Volumes/Raid/Claude/Applications/job-applications/Scripts/calendar_integration.py</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>9</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/tmp/calendarsync.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/calendarsync.error.log</string>
</dict>
</plist>
EOF

launchctl load ~/Library/LaunchAgents/com.obaisukar.calendarsync.plist
```

---

## 📱 Access Your Calendar Everywhere

### Web
- https://calendar.google.com

### iPhone/iPad
- Download **Google Calendar** app from App Store
- Sign in with obai@obaisukar.com

### Android
- Google Calendar (pre-installed)
- Sign in with obai@obaisukar.com

### Windows PC
1. Open Outlook
2. File → Account Settings → Account Settings
3. Click "New" → "Manual setup"
4. Choose "Google"
5. Enter: obai@obaisukar.com
6. Your Google Calendar syncs to Outlook

### Mac
1. System Preferences → Internet Accounts
2. Click "Google"
3. Sign in with obai@obaisukar.com
4. Check "Calendars"
5. Open Apple Calendar - events appear automatically

---

## 🔧 Troubleshooting

### "credentials.json not found"
**Solution:**
- Make sure you downloaded OAuth credentials from Google Cloud Console
- Rename to exactly `credentials.json` (not `client_secret_xxx.json`)
- Place in `/Volumes/Raid/Claude/Applications/job-applications/Scripts/`

### "No module named google"
**Solution:**
```bash
pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### "This app isn't verified" warning during authentication
**Solution:**
- This is normal for personal projects
- Click "Advanced" → "Go to Job Application Tracker (unsafe)"
- This is safe because YOU created the app

### Browser doesn't open during authentication
**Solution:**
```bash
# Copy the URL from terminal and paste in browser manually
```

### Events not appearing in calendar
**Solution:**
- Make sure you're signed into correct Google account (obai@obaisukar.com)
- Check "primary" calendar is visible
- Refresh Google Calendar page (Cmd+R or F5)

### Duplicate events being created
**Solution:**
- Current version creates new events each run
- Manually delete duplicates in Google Calendar
- Future enhancement: Check for existing events before creating

### "Access blocked: This app's request is invalid"
**Solution:**
- Go back to Google Cloud Console
- OAuth consent screen → Add test user: obai@obaisukar.com
- Make sure Calendar API is enabled

---

## 🔐 Security & Privacy

### What access does this have?
- **Calendar access only** - can read/write Google Calendar events
- **No access to:** Email, files, contacts, or other data

### Where are credentials stored?
- `credentials.json` - OAuth client ID (not sensitive, but keep private)
- `.calendar_token.pickle` - Your authentication token (DO NOT share)
- Both files are in `.gitignore` and won't be committed to GitHub

### How to revoke access?
1. Go to: https://myaccount.google.com/permissions
2. Find "Job Application Tracker"
3. Click "Remove Access"
4. Delete `.calendar_token.pickle` file

### Is this secure?
- ✅ Uses official Google OAuth 2.0 authentication
- ✅ Credentials stored locally (not in cloud)
- ✅ Standard Google Calendar API (same as other calendar apps)
- ✅ You control access - can revoke anytime

---

## 📊 Script Files Reference

### `calendar_integration.py`
Main script that:
- Reads `SPECIAL_REQUIREMENTS_TRACKER.md`
- Extracts jobs with deadlines
- Creates Google Calendar events
- Sets reminders based on urgency
- Color-codes events

**Location:** `/Volumes/Raid/Claude/Applications/job-applications/Scripts/calendar_integration.py`

### `CALENDAR_SETUP_GUIDE.md`
Detailed setup instructions (alternative version).

### `.calendar_token.pickle`
Authentication token (created automatically after first authentication).
**DO NOT DELETE** - or you'll need to re-authenticate.

### `credentials.json`
OAuth credentials from Google Cloud Console.
**REQUIRED** - download from Google Cloud Console.

---

## 🎯 Benefits Summary

✅ **Never miss deadlines** - Automatic reminders across all devices
✅ **Works everywhere** - PC, Mac, phone, web browser
✅ **Works when chat closed** - Independent of Claude Code
✅ **Smart reminders** - More frequent alerts for urgent deadlines
✅ **Visual organization** - Color-coded by urgency
✅ **Zero manual work** - Once set up, fully automated
✅ **Secure** - Uses official Google authentication

---

## ❓ FAQ

**Q: Do I need to run the script every time Claude adds a job?**
A: You can either run manually, ask Claude to sync, or set up daily auto-sync.

**Q: Will this work on my PC at work?**
A: Yes! Google Calendar syncs across all devices automatically.

**Q: What if I change a deadline in the tracker?**
A: Re-run the script. Note: Current version creates duplicates (manually delete old event).

**Q: Can I customize reminder times?**
A: Yes! Edit the `get_reminders()` function in `calendar_integration.py`.

**Q: Does this cost money?**
A: No! Google Calendar API is free for personal use (up to 1 million requests/day).

**Q: What if I don't want calendar events for certain jobs?**
A: Script only creates events for jobs with specific deadline dates (not "NOT SPECIFIED").

**Q: Can I use a different calendar app?**
A: Yes! Google Calendar syncs to Outlook, Apple Calendar, and most calendar apps.

---

## 📞 Getting Help

- **In Claude chat:** Just say "help with calendar setup" or "sync calendar"
- **View logs:** Check `/tmp/calendarsync.log` for errors
- **Documentation:** `Scripts/CALENDAR_SETUP_GUIDE.md` (detailed version)
- **Test script:** Run `python3 calendar_integration.py` to see if it works

---

## ✅ Next Steps When Ready

1. Follow **Step 1-10** above to complete setup
2. Test by running: `python3 Scripts/calendar_integration.py`
3. Check Google Calendar for events
4. Verify reminders work on your phone
5. (Optional) Set up daily auto-sync
6. Let Claude know it's working!

---

**Status:** Ready for setup - follow steps above when ready
**Estimated time:** 15 minutes
**Difficulty:** Easy (just follow steps)

**Questions?** Just ask Claude in chat anytime!
