const puppeteer = require('puppeteer');
const path = require('path');

async function convertToPDF() {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    
    const resumeHtmlPath = path.resolve(__dirname, 'meta_resume_only.html');
    const fileUrl = `file:///${resumeHtmlPath.replace(/\\/g, '/')}`;
    await page.goto(fileUrl);
    await page.pdf({
        path: path.join(__dirname, 'meta_resume_only_v3.pdf'),
        format: 'A4',
        printBackground: true,
        margin: {
            top: '0.35in',
            right: '0.45in',
            bottom: '0.35in',
            left: '0.45in'
        }
    });

    await browser.close();
    console.log('Compressed resume PDF created as meta_resume_only_v3.pdf');
}

convertToPDF().catch(console.error);