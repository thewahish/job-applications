const puppeteer = require('puppeteer');
const path = require('path');

async function convertToPDF() {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    
    const htmlPath = path.resolve(__dirname, 'observe_ai_final_clean.html');
    const pdfPath = path.resolve(__dirname, 'observe_ai_elegant_footer.pdf');
    
    await page.goto(`file://${htmlPath}`, { waitUntil: 'networkidle0' });
    
    await page.pdf({
        path: pdfPath,
        format: 'Letter',
        printBackground: true,
        margin: {
            top: '0.5in',
            bottom: '0.5in',
            left: '0.5in',
            right: '0.5in'
        }
    });
    
    await browser.close();
    console.log(`PDF saved to: ${pdfPath}`);
}

convertToPDF().catch(console.error);