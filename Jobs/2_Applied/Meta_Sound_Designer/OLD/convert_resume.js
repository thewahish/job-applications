const puppeteer = require('puppeteer');
const path = require('path');

async function convertToPDF() {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    
    // Convert resume only
    const resumeHtmlPath = path.resolve(__dirname, 'meta_resume_only.html');
    const fileUrl = `file:///${resumeHtmlPath.replace(/\\/g, '/')}`;
    await page.goto(fileUrl);
    await page.pdf({
        path: path.join(__dirname, 'meta_resume_only_v2.pdf'),
        format: 'A4',
        printBackground: true,
        margin: {
            top: '0.4in',
            right: '0.5in',
            bottom: '0.4in',
            left: '0.5in'
        }
    });

    await browser.close();
    console.log('Updated resume PDF created as meta_resume_only_v2.pdf');
}

convertToPDF().catch(console.error);