# Ultimate Resume Helper - Portable Setup

## 🚀 QUICK START (Works from any location)

### 1. SETUP
- Place this entire `Applications` folder anywhere you want
- All paths are relative - fully portable

### 2. COMMANDS

**Gemini Job Scraping:**
```bash
cd "[PATH_TO_THIS_APPLICATIONS_FOLDER]"
gemini -f gemini_job_scraper_prompt.md "Extract job from: [LINKEDIN_URL]"
```

**Claude Analysis:**
```
Working directory: [PATH_TO_THIS_APPLICATIONS_FOLDER]
Process Level 1 analysis for: [CompanyName_JobTitle_raw.md]
```

### 3. CURRENT LOCATION EXAMPLES

**If on D:\ drive:**
```bash
cd "D:\Applications"
gemini -f gemini_job_scraper_prompt.md "Extract job from: https://linkedin.com/jobs/view/123"
```

**If moved to C:\ drive:**
```bash
cd "C:\Applications"
gemini -f gemini_job_scraper_prompt.md "Extract job from: https://linkedin.com/jobs/view/123"
```

**If moved to USB/External drive:**
```bash
cd "E:\MyResumeSystem\Applications"
gemini -f gemini_job_scraper_prompt.md "Extract job from: https://linkedin.com/jobs/view/123"
```

## 📁 STRUCTURE
```
Applications/                           ← This folder (move anywhere)
├── README.md                          ← This file
├── ULTIMATE_RESUME_HELPER_MASTER_v2.md ← Complete system specifications
├── gemini_job_scraper_prompt.md       ← Gemini instructions
├── gemini_cli_instructions.md         ← Command reference
├── _TRACKING_MASTER.md               ← Analytics & learning
├── _PENDING_ANALYSIS/                ← Temporary job files
├── ObserveAI_Senior_Implementation_Manager/ ← Perfect template
└── [New application folders created here]
```

## ✅ PORTABILITY FEATURES
- **No hardcoded paths** - works from any drive/location
- **Relative file references** - internal links always work
- **Self-contained** - everything needed is in this folder
- **Copy anywhere** - drag folder to new location and resume work
- **Multi-user friendly** - each person can have their own copy

## 🎯 WORKFLOW
1. Move this folder wherever you want
2. `cd` into it from command line
3. Run Gemini commands to scrape jobs
4. Run Claude commands to process applications
5. All output stays within this folder structure

**No configuration needed - just works!**