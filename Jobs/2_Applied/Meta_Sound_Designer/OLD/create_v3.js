const puppeteer = require('puppeteer');
const path = require('path');

async function convertToPDF() {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    
    console.log('Generating v3 combined PDF with correct page structure...');
    const combinedHtmlPath = path.resolve(__dirname, 'meta_combined.html');
    const fileUrl = `file:///${combinedHtmlPath.replace(/\\/g, '/')}`;
    await page.goto(fileUrl);
    await page.pdf({
        path: path.join(__dirname, 'meta_combined_2025-09-01_v3.pdf'),
        format: 'A4',
        printBackground: true,
        margin: { top: '0.4in', right: '0.5in', bottom: '0.4in', left: '0.5in' }
    });

    await browser.close();
    console.log('✅ meta_combined_2025-09-01_v3.pdf - Perfect page structure!');
}

convertToPDF().catch(console.error);