#!/bin/bash

# Setup Script for Job Application Deadline Alerts
# This script configures automatic daily deadline monitoring

echo "🔧 Setting up Job Application Deadline Monitoring System"
echo ""

# Configuration
SCRIPT_DIR="/Volumes/Raid/Claude/Applications/job-applications/Scripts"
MONITOR_SCRIPT="$SCRIPT_DIR/deadline_monitor.sh"
LAUNCHD_PLIST="$HOME/Library/LaunchAgents/com.obaisukar.jobdeadlines.plist"

# Make monitor script executable
chmod +x "$MONITOR_SCRIPT"
echo "✅ Made deadline_monitor.sh executable"

# Create LaunchAgent plist for automatic daily execution
cat > "$LAUNCHD_PLIST" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.obaisukar.jobdeadlines</string>

    <key>ProgramArguments</key>
    <array>
        <string>/Volumes/Raid/Claude/Applications/job-applications/Scripts/deadline_monitor.sh</string>
    </array>

    <key>StartCalendarInterval</key>
    <array>
        <!-- Run at 9:00 AM daily -->
        <dict>
            <key>Hour</key>
            <integer>9</integer>
            <key>Minute</key>
            <integer>0</integer>
        </dict>
        <!-- Run at 5:00 PM daily -->
        <dict>
            <key>Hour</key>
            <integer>17</integer>
            <key>Minute</key>
            <integer>0</integer>
        </dict>
    </array>

    <key>StandardOutPath</key>
    <string>/tmp/jobdeadlines.log</string>

    <key>StandardErrorPath</key>
    <string>/tmp/jobdeadlines.error.log</string>
</dict>
</plist>
EOF

echo "✅ Created LaunchAgent plist at: $LAUNCHD_PLIST"

# Load the LaunchAgent
launchctl unload "$LAUNCHD_PLIST" 2>/dev/null  # Unload if already exists
launchctl load "$LAUNCHD_PLIST"
echo "✅ Loaded LaunchAgent (will run at 9 AM and 5 PM daily)"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ DEADLINE MONITORING SYSTEM SETUP COMPLETE!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📧 Email alerts will be sent to: obai@obaisukar.com"
echo "⏰ Monitoring schedule: 9:00 AM and 5:00 PM daily"
echo "📋 Tracking file: Jobs/SPECIAL_REQUIREMENTS_TRACKER.md"
echo ""
echo "🧪 To test immediately, run:"
echo "   $MONITOR_SCRIPT"
echo ""
echo "📝 To view logs:"
echo "   tail -f /tmp/jobdeadlines.log"
echo ""
echo "🛑 To disable alerts:"
echo "   launchctl unload $LAUNCHD_PLIST"
echo ""
echo "🔄 To re-enable alerts:"
echo "   launchctl load $LAUNCHD_PLIST"
echo ""
