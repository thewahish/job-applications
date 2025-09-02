@echo off
echo Starting Gemini for Job Application Processing...
echo Current directory: %CD%
echo.

cd /d "D:\Applications"

echo Project Context:
echo - Working in job application tracking system
echo - Use '_PENDING_ANALYSIS/' for scraped job data
echo - Instructions available in 'MD\gemini_job_scraper_prompt.md'
echo.
echo Ready to process job URLs! Just paste LinkedIn/Indeed links.
echo.

gemini -p "I'm working in Obai's job application tracking system at D:\Applications. When I provide job URLs (LinkedIn, Indeed, etc.), automatically scrape them and save the structured data to _PENDING_ANALYSIS/ following the format in MD\gemini_job_scraper_prompt.md. Process multiple URLs without asking. Ready to start!"

pause