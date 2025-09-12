# Job Application Duplicate Prevention Protocol

## ⚠️ CRITICAL RULE: NO DUPLICATES ALLOWED
Each job application folder should exist in **ONLY ONE** stage folder at any time.

## 🔍 Before Starting ANY Job Assessment

### 1. Run Duplicate Check Script
```bash
cd D:\Applications
bash Jobs/check_duplicates.sh
```

### 2. If Duplicates Found:
- **STOP** - Do not proceed with new assessments
- Identify which version is most complete:
  - Analysis Stage: Basic analysis.md only
  - Preparation Stage: Analysis + basic materials
  - Applied Stage: Analysis + complete application materials + README.md
  - Archive Stage: Final completed applications
  - Cancelled Stage: Withdrawn applications

### 3. Automatic Priority Resolution:
**Stage Priority Hierarchy (Highest to Lowest):**
1. **Archive (Priority: 5)** - Permanent completed applications
2. **Applied (Priority: 4)** - Active submitted applications  
3. **Preparation (Priority: 3)** - Ready for submission
4. **Analysis (Priority: 2)** - Basic assessment only
5. **Cancelled (Priority: 1)** - Withdrawn applications

**Automatic Resolution Logic:**
- ✅ **Higher Priority ALWAYS wins** - Lower priority version automatically deleted
- ⚠️ **Same Priority = Manual Review** - Script stops for human decision
- 🗑️ **Lower Priority Removed** - Script automatically cleans up duplicates

## 📋 Workflow Integration

### When User Reports Application Submitted:
1. **ALWAYS** run duplicate check first
2. Move from current stage to "3_Applied"
3. Verify no duplicates remain

### When Starting New Assessment:
1. **ALWAYS** run duplicate check first
2. Only proceed if clean
3. Create in "1_Analysis_Stage" only

### When Moving Between Stages:
1. Move folder completely (don't copy)
2. Verify source folder is completely removed
3. Update any references/links

## 🛠️ Tools Available

### Automatic Duplicate Detection & Resolution:
- Script: `Jobs/check_duplicates.sh`
- Scans all stage folders in priority order
- Identifies exact folder name matches (case-insensitive)
- **Automatically removes lower priority duplicates**
- Reports all actions taken
- Only requires manual intervention for same-priority conflicts

### Manual Verification:
```bash
find Jobs -name "*[Company_Name]*" -type d
```

## 🔄 Integration with Hierarchical Assessment Workflow

### MANDATORY: Before Starting ANY New Assessment:
```bash
bash Jobs/check_duplicates.sh
```
**This command MUST return "NO DUPLICATES FOUND" before proceeding**

### Standard Operating Procedure:
1. **User requests job assessment**
2. **Claude AUTOMATICALLY runs duplicate check FIRST**
3. **If duplicates found:** Clean up first, then proceed
4. **If clean:** Start assessment in appropriate category in Analysis stage
5. **Complete assessment workflow as normal**

### For New Job Creation:
1. **Determine job category** (IT_Technology, Audio_Sound, Creative_Media)
2. **Create in:** `Jobs/1_Analysis_Stage/[Category]/[Company_Role]/`
3. **All subsequent stage moves preserve category structure**

### When User Reports Application Submitted:
1. **ALWAYS run duplicate check first**
2. **Move folder from current stage/category to "3_Applied/[Same_Category]/"**
3. **Verify move completed successfully**
4. **Re-run duplicate check to confirm cleanup**

### Stage Progression Examples:
```bash
# Analysis → Preparation
Jobs/1_Analysis_Stage/IT_Technology/Microsoft_Director_IT/
    ↓
Jobs/2_Preparation_Stage/IT_Technology/Microsoft_Director_IT/

# Preparation → Applied  
Jobs/2_Preparation_Stage/Audio_Sound/Netflix_Sound_Designer/
    ↓
Jobs/3_Applied/Audio_Sound/Netflix_Sound_Designer/
```

## 📁 Folder Movement Commands

### Safe Move (recommended):
```bash
mv "Jobs/1_Analysis_Stage/[Company]" "Jobs/3_Applied/"
```

### Verify Move Completed:
```bash
ls "Jobs/1_Analysis_Stage/[Company]"  # Should show "No such file or directory"
ls "Jobs/3_Applied/[Company]"        # Should show folder contents
```

## 🚨 Emergency Cleanup

If duplicates are discovered:
1. Run comprehensive scan: `bash Jobs/check_duplicates.sh`
2. For each duplicate:
   - Compare folder contents
   - Keep most complete version
   - Delete duplicates from earlier stages
3. Re-run check to verify cleanup

---

**REMEMBER: Clean workspace = accurate workflow**