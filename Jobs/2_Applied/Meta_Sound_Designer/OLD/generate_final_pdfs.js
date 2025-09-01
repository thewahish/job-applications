const puppeteer = require('puppeteer');
const path = require('path');

async function convertAllToPDF() {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    
    console.log('Generating all Meta PDFs with version control naming...\n');
    
    // Convert creative cover (social media style)
    console.log('1. Converting creative cover (social media)...');
    const coverHtmlPath = path.resolve(__dirname, 'meta_space_optimized.html');
    const coverFileUrl = `file:///${coverHtmlPath.replace(/\\/g, '/')}`;
    await page.goto(coverFileUrl);
    await page.pdf({
        path: path.join(__dirname, 'meta_cover_creative_2025-09-01_v1.pdf'),
        format: 'A4',
        printBackground: true,
        margin: { top: '0.5in', right: '0.5in', bottom: '0.5in', left: '0.5in' }
    });
    console.log('✅ meta_cover_creative_2025-09-01_v1.pdf');
    
    // Convert resume only
    console.log('2. Converting resume only (ATS-friendly)...');
    const resumeHtmlPath = path.resolve(__dirname, 'meta_resume_only.html');
    const resumeFileUrl = `file:///${resumeHtmlPath.replace(/\\/g, '/')}`;
    await page.goto(resumeFileUrl);
    await page.pdf({
        path: path.join(__dirname, 'meta_resume_only_2025-09-01_v1.pdf'),
        format: 'A4',
        printBackground: true,
        margin: { top: '0.35in', right: '0.45in', bottom: '0.35in', left: '0.45in' }
    });
    console.log('✅ meta_resume_only_2025-09-01_v1.pdf');
    
    // Convert combined cover + resume
    console.log('3. Converting combined cover + resume...');
    const combinedHtmlPath = path.resolve(__dirname, 'meta_combined.html');
    const combinedFileUrl = `file:///${combinedHtmlPath.replace(/\\/g, '/')}`;
    await page.goto(combinedFileUrl);
    await page.pdf({
        path: path.join(__dirname, 'meta_combined_2025-09-01_v1.pdf'),
        format: 'A4',
        printBackground: true,
        margin: { top: '0.4in', right: '0.5in', bottom: '0.4in', left: '0.5in' }
    });
    console.log('✅ meta_combined_2025-09-01_v1.pdf');

    await browser.close();
    console.log('\n🚀 All Meta PDFs generated successfully with version control naming!');
    console.log('\nGenerated files:');
    console.log('- meta_cover_creative_2025-09-01_v1.pdf (Creative social media cover)');
    console.log('- meta_resume_only_2025-09-01_v1.pdf (ATS-friendly resume)');
    console.log('- meta_combined_2025-09-01_v1.pdf (Traditional cover + resume)');
}

convertAllToPDF().catch(console.error);