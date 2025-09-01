# Gemini CLI Integration Instructions

## SETUP & WORKFLOW

### 1. GEMINI CLI COMMAND FORMAT
```bash
cd "D:\Applications"
gemini -f gemini_job_scraper_prompt.md "Extract job information from this LinkedIn URL: [PASTE_URL_HERE]"
```

**PORTABLE ALTERNATIVE (works from any drive/location):**
```bash
cd "[PATH_TO_YOUR_APPLICATIONS_FOLDER]"
gemini -f gemini_job_scraper_prompt.md "Extract job information from this LinkedIn URL: [PASTE_URL_HERE]"
```

### 2. EXPECTED OUTPUT
Gemini will create a file in:
```
_PENDING_ANALYSIS/[CompanyName]_[JobTitle]_raw.md
```

### 3. CLAUDE CODE WORKFLOW
After Gemini creates the raw file, provide Claude Code with:
```
"Working directory: [YOUR_APPLICATIONS_FOLDER_PATH]
Process Level 1 analysis for: [CompanyName]_[JobTitle]_raw.md"
```

**Example:**
```
"Working directory: D:\Applications
Process Level 1 analysis for: Microsoft_Cloud_Architect_raw.md"
```

Claude will:
1. Read the raw file from _PENDING_ANALYSIS
2. Calculate compatibility score (0-100%)
3. Create PROCEED (≥70%) or -NO (<70%) folder in Jobs/1_Analysis_Stage/
4. Generate all tracking documents and update CSV tracker
5. Move raw file to appropriate status folder
6. Update _JOB_TRACKER_MASTER.csv with analysis results

## BATCH PROCESSING WORKFLOW

### Phase 1: Information Gathering (You + Gemini)
```bash
# Process multiple jobs at once
gemini -f gemini_job_scraper_prompt.md "Extract job info from: [URL1]"
gemini -f gemini_job_scraper_prompt.md "Extract job info from: [URL2]"
gemini -f gemini_job_scraper_prompt.md "Extract job info from: [URL3]"
# Continue for as many jobs as needed
```

### Phase 2: Compatibility Analysis (You + Claude Code)
```
"Process all pending analyses in _PENDING_ANALYSIS folder"
```

Claude will batch process all raw files, creating:
- Individual PROCEED/NO folders in Jobs/1_Analysis_Stage/ for each
- Complete tracking documents for all applications
- Updated _JOB_TRACKER_MASTER.csv with compatibility scores
- Updated HTML dashboard with new statistics

## QUALITY CONTROL CHECKLIST

### Before Running Gemini:
- [ ] LinkedIn URL is accessible and complete
- [ ] _PENDING_ANALYSIS folder exists
- [ ] Gemini CLI is properly configured

### After Gemini Processing:
- [ ] Raw file created in correct location
- [ ] File name follows naming convention
- [ ] All required sections are populated
- [ ] Technical requirements are detailed

### Before Claude Processing:
- [ ] Raw file contains sufficient information
- [ ] Company name and job title are clear
- [ ] Salary and location information captured

## TROUBLESHOOTING

### If Gemini Can't Access LinkedIn:
1. Try opening URL manually first
2. Check if login is required
3. Use alternative job board URL if available
4. Create manual raw file with available information

### If File Naming Issues:
1. Check for special characters in company/job names
2. Ensure underscores replace spaces
3. Verify _PENDING_ANALYSIS folder exists
4. Check file permissions

### If Claude Can't Process:
1. Verify raw file format matches expected structure
2. Check that all required sections exist
3. Ensure file is in correct directory
4. Validate company name and job title formatting

## EFFICIENCY TIPS

### Morning Batch Processing:
1. **8:00 AM**: Run Gemini on 5-10 job URLs
2. **8:30 AM**: Review generated raw files
3. **9:00 AM**: Start Claude processing session
4. **9:30 AM**: Review compatibility results
5. **10:00 AM**: Process PROCEED applications (logo placement + generation)
6. **11:00 AM**: Move completed applications to Jobs/2_Applied/ after submission

### Token Optimization:
- Process multiple raw files per Claude session
- Use batch commands when possible
- Focus on high-compatibility roles first
- Skip obviously poor matches quickly

## EXAMPLE WORKFLOW
```bash
# Step 1: Scrape multiple jobs
gemini -f gemini_job_scraper_prompt.md "Extract: https://linkedin.com/jobs/view/123456"
gemini -f gemini_job_scraper_prompt.md "Extract: https://linkedin.com/jobs/view/789012"

# Step 2: Process with Claude
# "Process all pending analyses - batch mode"

# Step 3: Handle PROCEED results
# Place logos in approved folders
# Generate final applications
```

This workflow should achieve **10+ job analyses per session** with minimal token usage!

## STATUS TRACKING INTEGRATION

### Automatic Folder Movement
After Claude completes Level 1 analysis, jobs move through this progression:
```
_PENDING_ANALYSIS/Company_Job_raw.md
    ↓
Jobs/1_Analysis_Stage/Company_Job/ (≥70% compatibility)
    ↓ (after application generation and submission)
Jobs/2_Applied/Company_Job/
    ↓ (after company response)
Jobs/3_Accepted/Company_Job/ OR Jobs/4_Rejected/Company_Job/
```

### CSV Tracker Auto-Updates
Every status change automatically updates:
- `_JOB_TRACKER_MASTER.csv` with dates and status changes
- `_JOB_DASHBOARD_TRACKER.html` with live statistics
- Individual folder tracking documents

### Status Management Commands
```bash
# Move application to Applied status (after submission)
"Move Microsoft_Cloud_Architect to Applied status - submitted today"

# Update with company response  
"Update ObserveAI application - received rejection email"

# Update with interview scheduling
"Update Meta application - phone interview scheduled for Friday"
```

### Dashboard Monitoring  
Open `_JOB_DASHBOARD_TRACKER.html` in browser to:
- View real-time application statistics  
- Monitor response times across all applications
- Track success patterns and improvement areas
- Export updated CSV for external analysis