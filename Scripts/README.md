# Job Application Automation Scripts

This directory contains automation scripts for managing job application deadlines and notifications.

---

## 📧 Deadline Monitoring System

Automatically checks for approaching job application deadlines and sends email alerts.

### Quick Setup (One-Time)

```bash
cd /Volumes/Raid/Claude/Applications/job-applications/Scripts
./setup_deadline_alerts.sh
```

This will:
- Configure automatic deadline monitoring
- Set up daily email alerts (9 AM and 5 PM)
- Enable background monitoring via macOS LaunchAgent

### How It Works

1. **`deadline_monitor.sh`** - Scans `SPECIAL_REQUIREMENTS_TRACKER.md` for deadlines
2. **Email alerts sent when:**
   - 🚨 **URGENT** deadlines detected (apply today/tomorrow)
   - ⏰ **HIGH PRIORITY** deadlines detected (within 3-7 days)
   - 📅 **MODERATE** deadlines detected (within 1-2 weeks)

3. **Alert schedule:** Twice daily at 9:00 AM and 5:00 PM

### Manual Testing

Test the deadline monitor immediately:

```bash
./deadline_monitor.sh
```

### Configuration

Edit email address in `deadline_monitor.sh`:
```bash
EMAIL="obai@obaisukar.com"  # Change this line
```

Edit monitoring schedule in `setup_deadline_alerts.sh` (LaunchAgent plist section):
```xml
<key>Hour</key>
<integer>9</integer>  <!-- Change hour here -->
```

### Troubleshooting

**Check if LaunchAgent is running:**
```bash
launchctl list | grep jobdeadlines
```

**View logs:**
```bash
tail -f /tmp/jobdeadlines.log
tail -f /tmp/jobdeadlines.error.log
```

**Restart monitoring:**
```bash
launchctl unload ~/Library/LaunchAgents/com.obaisukar.jobdeadlines.plist
launchctl load ~/Library/LaunchAgents/com.obaisukar.jobdeadlines.plist
```

**Disable monitoring:**
```bash
launchctl unload ~/Library/LaunchAgents/com.obaisukar.jobdeadlines.plist
```

**Re-enable monitoring:**
```bash
launchctl load ~/Library/LaunchAgents/com.obaisukar.jobdeadlines.plist
```

---

## 🔔 Email Requirements

The monitoring system uses macOS built-in `mail` command. Make sure:

1. **macOS Mail.app** is configured with your email account
2. **Email account** (obai@obaisukar.com) is set up and working
3. **Test email manually:**
   ```bash
   echo "Test email" | mail -s "Test Subject" obai@obaisukar.com
   ```

If emails aren't sending, configure Mail.app with your email account first.

---

## 📝 Deadline Format in Tracker

For the monitoring system to work, deadlines in `SPECIAL_REQUIREMENTS_TRACKER.md` must follow this format:

```markdown
**Application Deadline:** 🚨 October 2, 2025 (APPLY TODAY)
**Application Deadline:** ⏰ October 5, 2025 (3 days remaining)
**Application Deadline:** 📅 October 15, 2025 (2 weeks)
**Application Deadline:** ⏳ NOT SPECIFIED (Apply within 24-48 hours recommended)
```

The script scans for these emoji indicators:
- 🚨 = URGENT (triggers immediate alert)
- ⏰ = HIGH PRIORITY (triggers alert)
- 📅 = MODERATE (included in alert summary)
- ⏳ = FLEXIBLE (no alert)

---

## 🎯 Future Enhancements

Possible additions:
- Slack/Discord webhook notifications
- SMS alerts via Twilio
- Calendar event creation
- Weekly summary reports
- Application status tracking
- Success rate analytics

---

**Last Updated:** October 1, 2025
