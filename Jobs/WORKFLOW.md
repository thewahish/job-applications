# Job Application Workflow

## 📋 STAGES OVERVIEW

### 🔍 Stage 1: ANALYSIS (Jobs/1_Analysis_Stage/)
- Job posting analysis and compatibility scoring
- Company research and requirements mapping
- Strategic assessment and ranking

### 🎯 Stage 2: PREPARATION (Jobs/1_Preparation_Stage/)
- **WAIT FOR USER TO SELECT POSITION**
- Create targeted resume with role-specific focus
- Write custom cover letter with company research
- Design company-branded materials (colors, visual identity)
- Build combined HTML file (cover letter + resume)
- Generate PDF versions ready for submission
- **REQUIRE USER APPROVAL** before proceeding

### ✅ Stage 3: APPLICATION (Jobs/2_Applied/)
- **ONLY move here after user explicitly confirms "applied"**
- User must confirm they submitted the application
- Store final submitted materials
- Track application status and follow-ups

## 🚨 CRITICAL RULES
1. **NEVER assume user wants to apply** - always ask first
2. **NEVER move to applied folder** until user confirms submission
3. **ALWAYS wait for approval** after creating preparation materials
4. **ASK before creating materials** - which position should we prepare for?

## 📁 FOLDER STRUCTURE
```
Jobs/
├── 1_Analysis_Stage/          # Completed analyses
├── 1_Preparation_Stage/       # Materials ready for review
└── 2_Applied/                 # Confirmed submissions only
```

## 🎨 COMPLETE APPLICATION PACKAGE
Each preparation folder should contain:
- **`README.md`** - Application tracking with URL, change log, brand elements
- `[company]_resume_targeted.html` - Role-focused resume
- `[company]_cover_letter.html` - Custom cover letter  
- `[company]_combined_complete.html` - Cover letter + resume
- `[company]_resume.pdf` - PDF version
- `[company]_combined.pdf` - PDF version
- Company-branded styling with their colors/identity

## 📋 README TRACKING REQUIREMENTS
**MANDATORY: Every job folder MUST have README.md at root level**

### README Must Include:
1. **Application URL** - Direct link to apply (at the top)
2. **File inventory** - List all materials with completion status
3. **Brand elements** - Company colors and visual identity
4. **Key positioning** - Strategic messaging and selling points
5. **Change log** - All modifications with dates/times
6. **Next steps** - Action items and follow-up timeline

### Location Rule:
- README.md at **ROOT** of job folder (NOT in OLD subfolder)
- Update README with every change made to materials
- Track progression through workflow stages