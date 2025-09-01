const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

async function extractLogo() {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    
    try {
        await page.goto('https://www.observe.ai', { waitUntil: 'networkidle0' });
        
        // Look for common logo selectors
        const logoSelectors = [
            'img[alt*="logo" i]',
            'img[src*="logo" i]',
            '.logo img',
            '[class*="logo"] img',
            'header img',
            'nav img',
            'img[alt*="observe" i]',
            'svg[class*="logo"]'
        ];
        
        let logoFound = false;
        
        for (const selector of logoSelectors) {
            try {
                const logoElement = await page.$(selector);
                if (logoElement) {
                    const logoSrc = await page.evaluate(el => el.src || el.currentSrc, logoElement);
                    
                    if (logoSrc && !logoSrc.includes('data:image')) {
                        console.log(`Found logo: ${logoSrc}`);
                        
                        // Download the logo
                        const logoResponse = await page.goto(logoSrc);
                        const logoBuffer = await logoResponse.buffer();
                        
                        // Determine file extension
                        const url = new URL(logoSrc);
                        let ext = path.extname(url.pathname) || '.png';
                        if (!ext.match(/\.(png|jpg|jpeg|svg|gif)$/i)) {
                            ext = '.png';
                        }
                        
                        const logoPath = path.resolve(__dirname, `observe_ai_logo${ext}`);
                        fs.writeFileSync(logoPath, logoBuffer);
                        
                        console.log(`Logo saved to: ${logoPath}`);
                        logoFound = true;
                        break;
                    }
                }
            } catch (e) {
                // Continue to next selector
                continue;
            }
        }
        
        if (!logoFound) {
            // Take a screenshot of the header area as fallback
            await page.setViewport({ width: 1200, height: 800 });
            const headerElement = await page.$('header, nav, [class*="header"], [class*="nav"]');
            
            if (headerElement) {
                await headerElement.screenshot({ 
                    path: path.resolve(__dirname, 'observe_ai_header.png'),
                    type: 'png'
                });
                console.log('Header screenshot saved as fallback');
            } else {
                // Screenshot top portion of page
                await page.screenshot({ 
                    path: path.resolve(__dirname, 'observe_ai_top_section.png'),
                    clip: { x: 0, y: 0, width: 1200, height: 200 },
                    type: 'png'
                });
                console.log('Top section screenshot saved as fallback');
            }
        }
        
    } catch (error) {
        console.error('Error extracting logo:', error);
    }
    
    await browser.close();
}

extractLogo().catch(console.error);