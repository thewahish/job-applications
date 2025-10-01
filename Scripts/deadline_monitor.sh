#!/bin/bash

# Job Application Deadline Monitor
# Checks SPECIAL_REQUIREMENTS_TRACKER.md for approaching deadlines and sends email alerts

# Configuration
EMAIL="obai@obaisukar.com"
TRACKER_FILE="/Volumes/Raid/Claude/Applications/job-applications/Jobs/SPECIAL_REQUIREMENTS_TRACKER.md"
TEMP_FILE="/tmp/deadline_check_$(date +%s).txt"

# Get today's date
TODAY=$(date +%Y-%m-%d)
TODAY_EPOCH=$(date -j -f "%Y-%m-%d" "$TODAY" +%s)

# Function to extract deadlines from tracker
check_deadlines() {
    local urgent_jobs=""
    local high_priority_jobs=""
    local moderate_priority_jobs=""

    # Read the tracker file and extract deadline information
    while IFS= read -r line; do
        # Look for job titles (lines starting with ###)
        if [[ $line =~ ^###[[:space:]](.+)$ ]]; then
            current_job="${BASH_REMATCH[1]}"
        fi

        # Look for deadline lines
        if [[ $line =~ \*\*Application[[:space:]]Deadline:\*\*[[:space:]](.+)$ ]]; then
            deadline_info="${BASH_REMATCH[1]}"

            # Check if deadline contains 🚨 URGENT indicator
            if [[ $deadline_info == *"🚨"* ]]; then
                urgent_jobs="${urgent_jobs}\n- ${current_job}: ${deadline_info}"
            fi

            # Check if deadline contains ⏰ HIGH PRIORITY indicator
            if [[ $deadline_info == *"⏰"* ]] && [[ $deadline_info != *"NOT SPECIFIED"* ]]; then
                high_priority_jobs="${high_priority_jobs}\n- ${current_job}: ${deadline_info}"
            fi

            # Check if deadline contains 📅 MODERATE indicator
            if [[ $deadline_info == *"📅"* ]]; then
                moderate_priority_jobs="${moderate_priority_jobs}\n- ${current_job}: ${deadline_info}"
            fi
        fi
    done < "$TRACKER_FILE"

    # Build email body
    local email_body=""
    local send_email=false

    if [[ -n "$urgent_jobs" ]]; then
        email_body="${email_body}🚨 URGENT DEADLINES (Apply Today/Tomorrow):\n${urgent_jobs}\n\n"
        send_email=true
    fi

    if [[ -n "$high_priority_jobs" ]]; then
        email_body="${email_body}⏰ HIGH PRIORITY DEADLINES (This Week):\n${high_priority_jobs}\n\n"
        send_email=true
    fi

    if [[ -n "$moderate_priority_jobs" ]]; then
        email_body="${email_body}📅 MODERATE DEADLINES (Next 2 Weeks):\n${moderate_priority_jobs}\n\n"
    fi

    # If there are urgent or high priority deadlines, send email
    if [[ "$send_email" == true ]]; then
        echo -e "Subject: Job Application Deadline Alert - $(date +%Y-%m-%d)\n\n${email_body}\n\nFull details: ${TRACKER_FILE}\n\nThis is an automated reminder from your job application tracking system." > "$TEMP_FILE"

        # Send email using macOS mail command
        cat "$TEMP_FILE" | mail -s "🚨 Job Application Deadline Alert - Action Required" "$EMAIL"

        echo "✅ Deadline alert email sent to $EMAIL"
        rm "$TEMP_FILE"
        return 0
    else
        echo "✓ No urgent deadlines found. All clear!"
        return 1
    fi
}

# Run the deadline check
check_deadlines

exit 0
