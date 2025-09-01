#!/usr/bin/env node
/**
 * Portable HTML to PDF Converter (Node.js version)
 * Converts HTML files to PDF using Puppeteer
 * Supports single files and batch processing
 */

const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs').promises;
const glob = require('glob');

async function convertSingleHTML(htmlPath, outputDir = null) {
    try {
        const resolvedPath = path.resolve(htmlPath);
        const stats = await fs.stat(resolvedPath);
        
        if (!stats.isFile()) {
            console.log(`[error] Not a file: ${htmlPath}`);
            return false;
        }

        if (outputDir === null) {
            outputDir = path.dirname(resolvedPath);
        }

        const fileName = path.basename(resolvedPath, '.html');
        const pdfPath = path.join(outputDir, `${fileName}.pdf`);
        
        console.log(`[info] Converting: ${path.basename(htmlPath)}`);
        console.log(`[info] Output: ${path.basename(pdfPath)}`);

        const browser = await puppeteer.launch({ headless: true });
        const page = await browser.newPage();
        
        await page.goto(`file://${resolvedPath}`, { 
            waitUntil: 'networkidle0',
            timeout: 60000 
        });
        
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
        console.log(`[success] PDF created: ${path.basename(pdfPath)}`);
        return true;
        
    } catch (error) {
        console.log(`[error] Failed to convert ${htmlPath}: ${error.message}`);
        return false;
    }
}

async function batchConvertFolder(folderPath, pattern = '*.html') {
    try {
        const resolvedFolder = path.resolve(folderPath);
        const stats = await fs.stat(resolvedFolder);
        
        if (!stats.isDirectory()) {
            console.log(`[error] Not a directory: ${folderPath}`);
            return;
        }

        const searchPattern = path.join(resolvedFolder, pattern);
        const htmlFiles = glob.sync(searchPattern);
        
        if (htmlFiles.length === 0) {
            console.log(`[info] No HTML files found in: ${folderPath}`);
            return;
        }

        console.log(`[info] Found ${htmlFiles.length} HTML files`);
        console.log(`[info] Processing folder: ${resolvedFolder}`);
        
        let successCount = 0;
        for (const htmlFile of htmlFiles) {
            const success = await convertSingleHTML(htmlFile, resolvedFolder);
            if (success) successCount++;
            console.log(); // Add spacing
        }
        
        console.log(`[summary] Successfully converted ${successCount}/${htmlFiles.length} files`);
        
    } catch (error) {
        console.log(`[error] Failed to process folder ${folderPath}: ${error.message}`);
    }
}

function showHelp() {
    const helpText = `
🚀 PORTABLE HTML TO PDF CONVERTER (Node.js)

USAGE OPTIONS:

1. SINGLE FILE:
   node batch_html_to_pdf.js filename.html
   node batch_html_to_pdf.js "C:\\\\path\\\\to\\\\file.html"

2. BATCH CONVERT CURRENT FOLDER:
   node batch_html_to_pdf.js .

3. BATCH CONVERT SPECIFIC FOLDER:
   node batch_html_to_pdf.js "C:\\\\path\\\\to\\\\folder"

4. HELP:
   node batch_html_to_pdf.js --help

FEATURES:
- Letter format (8.5" x 11") with 0.5" margins
- Background graphics included
- Optimized for resumes and cover letters
- Portable - works from any location

REQUIREMENTS:
- Node.js 14+
- npm install puppeteer
`;
    console.log(helpText);
}

async function main() {
    if (process.argv.length > 2) {
        const arg = process.argv[2].trim();
        
        if (arg === '--help' || arg === '-h' || arg === 'help') {
            showHelp();
            return;
        }
        
        if (arg === '.') {
            await batchConvertFolder(process.cwd());
            return;
        }
        
        try {
            const stats = await fs.stat(arg);
            if (stats.isFile() && path.extname(arg).toLowerCase() === '.html') {
                await convertSingleHTML(arg);
            } else if (stats.isDirectory()) {
                await batchConvertFolder(arg);
            } else {
                console.log(`[error] Invalid target: ${arg}`);
            }
        } catch (error) {
            console.log(`[error] Target not found: ${arg}`);
        }
    } else {
        // Interactive mode
        const readline = require('readline');
        const rl = readline.createInterface({
            input: process.stdin,
            output: process.stdout
        });
        
        rl.question('Enter HTML file or folder path (or "help"): ', async (input) => {
            const trimmed = input.trim().replace(/['"]/g, '');
            if (trimmed.toLowerCase() === 'help') {
                showHelp();
            } else {
                process.argv[2] = trimmed;
                await main();
            }
            rl.close();
        });
    }
}

if (require.main === module) {
    main().catch(console.error);
}

module.exports = { convertSingleHTML, batchConvertFolder };