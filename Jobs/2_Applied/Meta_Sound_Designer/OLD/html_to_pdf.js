const puppeteer = require('puppeteer');
const path = require('path');

async function convertToPDF() {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    
    // Convert resume only
    const resumeHtmlPath = path.resolve(__dirname, 'meta_resume_only.html');
    await page.goto(`file:///${resumeHtmlPath.replace(/\\/g, '/')}`);
    await page.pdf({
        path: path.join(__dirname, 'meta_resume_only.pdf'),
        format: 'A4',
        printBackground: true,
        margin: {
            top: '0.4in',
            right: '0.5in',
            bottom: '0.4in',
            left: '0.5in'
        }
    });

    // Convert combined cover + resume
    const combinedHtmlPath = path.join(__dirname, 'meta_combined.html');
    await page.goto(`file://${combinedHtmlPath}`);
    await page.pdf({
        path: path.join(__dirname, 'meta_combined.pdf'),
        format: 'A4',
        printBackground: true,
        margin: {
            top: '0.5in',
            right: '0.5in', 
            bottom: '0.5in',
            left: '0.5in'
        }
    });

    await browser.close();
    console.log('PDFs generated successfully!');
}

convertToPDF().catch(console.error);