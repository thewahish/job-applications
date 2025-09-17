import os

# URL mapping from APPLICATION_URLS_MASTER.txt
url_map = {
    # Audio/Sound
    "Lightspeed_Studios_Sound_Designer": "https://www.indeed.com/viewjob?jk=8329b427511ef180",
    "Valve_Software_Sound_Designer": "https://www.indeed.com/viewjob?jk=ac6e1a2e53db899f",
    "Meta_Interaction_UX_Sound_Designer": "https://www.indeed.com/viewjob?jk=5d28315db52528b9",
    "Union_Company_Sound_Engineer": "https://www.indeed.com/viewjob?jk=6a5bce1a8e4e9ce0",
    "Tencent_Sound_Designer_III": "https://www.linkedin.com/jobs/view/sound-designer-iii-at-tencent-4225718668",
    "Juilliard_Audio_Technician": "https://www.linkedin.com/jobs/view/audio-technician-sound-shop-at-the-juilliard-school-4213984694",
    "Lensa_Sound_Designer": "https://www.linkedin.com/jobs/view/sound-designer-at-lensa-4245455795",
    "MIX_UNION_Studio_Assistant": "https://www.indeed.com/viewjob?jk=e2d3b9bf8b4630f0",
    "QuaverEd_Music_Producer": "https://www.linkedin.com/jobs/view/music-producer-at-quavered-4283335511",
    "Ramsey_Solutions_Audio_Engineer": "https://www.indeed.com/viewjob?jk=79debc5b0e497852",

    # IT Technology
    "Naviant_Director_IT": "https://www.indeed.com/viewjob?jk=f68104c3e94a7c2e",
    "Mutual_Group_Director_IT": "https://www.indeed.com/viewjob?jk=156b2b00bbb116bd",
    "Business_Wire_Director_IT": "https://www.indeed.com/viewjob?jk=a1f16c03067b3e92",
    "Deloitte_Enterprise_Architect": "https://www.indeed.com/viewjob?jk=5247518f709ca453",
    "Credit_One_Bank_IT_Enterprise_Architect_IV": "https://www.indeed.com/viewjob?jk=4740b1c52a657465",
    "Headway_Director_IT": "https://www.indeed.com/viewjob?jk=a8dbd025a6df4f07",
    "Adyen_Head_Technical_Support_Americas": "https://jobright.ai/jobs/info/68b9ddc65f383274918617ce",

    # Creative/Media
    "audiio_Creative_Producer": "https://www.linkedin.com/jobs/view/creative-producer-at-audiio-4282482885",
    "Boys_Girls_Clubs_Music_Studio_Director": "https://www.indeed.com/viewjob?jk=c5a01989a78b2992",
    "Coastal_Sound_Studios": "https://www.linkedin.com/jobs/view/coastal-sound-studios-llc-at-coastal-sound-studios-4212286595",
}

def clean_company_name(folder_name):
    """Extract clean company name from folder name"""
    parts = folder_name.replace("_", " ")
    # Common patterns to clean up
    parts = parts.replace("IT Enterprise Architect IV", "").replace("IT Enterprise Architect", "")
    parts = parts.replace("Director IT", "").replace("Head Technical Support Americas", "")
    parts = parts.replace("Sound Designer III", "Sound Designer").replace("Sound Designer", "")
    parts = parts.replace("Audio Engineer", "").replace("Audio Technician", "")
    parts = parts.replace("Studio Assistant", "").replace("Music Producer", "")
    parts = parts.replace("Creative Producer", "").replace("Music Studio Director", "")
    return parts.strip()

def get_job_title(folder_name):
    """Extract job title from folder name"""
    # Map common patterns
    if "Director_IT" in folder_name:
        return "Director of IT"
    elif "Sound_Designer" in folder_name:
        if "Lead" in folder_name:
            return "Lead Sound Designer"
        elif "III" in folder_name:
            return "Sound Designer III"
        elif "UX" in folder_name:
            return "Interaction UX Sound Designer"
        else:
            return "Sound Designer"
    elif "Audio_Engineer" in folder_name:
        return "Audio Engineer"
    elif "Audio_Technician" in folder_name:
        return "Audio Technician"
    elif "Enterprise_Architect" in folder_name:
        if "IV" in folder_name:
            return "IT Enterprise Architect IV"
        else:
            return "Enterprise Architect"
    elif "Creative_Producer" in folder_name:
        return "Creative Producer"
    elif "Music_Producer" in folder_name:
        return "Music Producer"
    elif "Studio_Assistant" in folder_name:
        return "Studio Assistant"
    elif "Music_Studio_Director" in folder_name:
        return "Music Studio Director"
    elif "Head_Technical_Support" in folder_name:
        return "Head of Technical Support Americas"
    elif "Sound_Engineer" in folder_name:
        return "Sound Engineer"
    elif "Integration_Support_Manager" in folder_name:
        return "Manager Integration Support Engineering"
    elif "Implementation_Manager" in folder_name:
        return "Senior Implementation Manager"
    elif "Theatrical_Sound_Manager" in folder_name:
        return "Theatrical Sound Manager"
    else:
        # Default: convert underscores to spaces
        return folder_name.replace("_", " ")

def create_readme(folder_path, folder_name, stage):
    """Create or update README.md for a job folder"""
    readme_path = os.path.join(folder_path, "README.md")

    # Get URL from mapping or mark as needed
    url = url_map.get(folder_name, "URL needed - Search company careers page")

    # Clean up names
    company = clean_company_name(folder_name)
    job_title = get_job_title(folder_name)

    # Determine category for positioning
    if "Audio" in folder_path or "Sound" in folder_path:
        positioning = "- Sound engineering expertise with 20+ years experience\n- 'Sound is what I breathe' positioning\n- 301M+ views media production experience"
    elif "IT_Technology" in folder_path:
        positioning = "- 'Technology is my DNA' positioning\n- IT Director experience with 99.8% uptime\n- Independent consulting since 2000"
    elif "Creative_Media" in folder_path:
        positioning = "- Creative media production leadership\n- Karazah Channel with 715K subscribers\n- Award-winning content creation"
    else:
        positioning = "- Multi-disciplinary expertise\n- Proven leadership and innovation\n- Cross-cultural experience"

    content = f"""# {company} - {job_title}

**Application URL:** {url}

## Application Details
- **Date Created:** September 2025
- **Stage:** {stage}
- **Status:** Active

## Files Created
- analysis.md - Compatibility analysis
- {folder_name.lower()}_resume_ats.html - ATS-optimized resume

## Key Positioning
{positioning}

## Next Steps
- Request company logo for premium materials
- Create premium cover letter
- Submit application"""

    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created/Updated: {readme_path}")

# Process all job folders
base_path = "D:/Applications/Jobs"

# Process Analysis Stage
for category in ["Audio_Sound", "IT_Technology", "Creative_Media"]:
    category_path = os.path.join(base_path, "1_Analysis_Stage", category)
    if os.path.exists(category_path):
        for folder in os.listdir(category_path):
            folder_path = os.path.join(category_path, folder)
            if os.path.isdir(folder_path):
                create_readme(folder_path, folder, "Analysis")

# Process Applied Stage (including Meta folder)
applied_path = os.path.join(base_path, "3_Applied")
if os.path.exists(applied_path):
    for folder in os.listdir(applied_path):
        folder_path = os.path.join(applied_path, folder)
        if os.path.isdir(folder_path):
            # Special handling for Meta
            if "Meta" in folder:
                url = "LinkedIn posting - Search for 'Creative Audio-AI Voice and Audio Lead at Meta'"
            else:
                url = url_map.get(folder, "Application submitted - Check email for confirmation")

            readme_path = os.path.join(folder_path, "README.md")
            company = clean_company_name(folder)
            job_title = get_job_title(folder)

            content = f"""# {company} - {job_title}

**Application URL:** {url}

## Application Details
- **Date Created:** September 2025
- **Stage:** Applied
- **Status:** Submitted

## Files Created
- All application materials completed
- Premium cover letter created
- Combined resume and cover letter submitted

## Key Positioning
- Role-specific positioning applied
- Company branding integrated
- Testimonials included

## Next Steps
- Monitor for response
- Prepare for interview
- Follow up if needed after 1 week"""

            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Created/Updated: {readme_path}")

print("\nAll README.md files have been created/updated!")