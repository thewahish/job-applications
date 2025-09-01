#!/usr/bin/env python3
"""
Portable HTML to PDF Converter
Converts HTML files to PDF using Playwright
Supports single files, batch processing, and folder scanning
"""
import sys
import pathlib
import asyncio
import traceback
import glob
import os
from playwright.async_api import async_playwright, TimeoutError as PWTimeout

async def convert_single_html(html_path: pathlib.Path, output_dir: pathlib.Path = None) -> bool:
    """Convert a single HTML file to PDF"""
    if not html_path.exists():
        print(f"[error] File not found: {html_path}")
        return False
        
    if output_dir is None:
        output_dir = html_path.parent
        
    # Generate PDF filename based on HTML filename
    pdf_path = output_dir / f"{html_path.stem}.pdf"
    url = html_path.as_uri()
    
    print(f"[info] Converting: {html_path.name}")
    print(f"[info] Output: {pdf_path}")
    
    try:
        async with async_playwright() as pw:
            browser = await pw.chromium.launch(headless=True)
            page = await browser.new_page()
            
            try:
                await page.goto(url, wait_until="networkidle", timeout=60000)
            except PWTimeout:
                print("[warn] NetworkIdle timeout, trying 'load'...")
                await page.goto(url, wait_until="load", timeout=30000)
            
            # Convert to PDF with optimized settings
            await page.pdf(
                path=str(pdf_path),
                format="Letter",  # US Letter format
                print_background=True,
                prefer_css_page_size=False,  # Use Letter format consistently
                margin={
                    "top": "0.5in",
                    "bottom": "0.5in", 
                    "left": "0.5in",
                    "right": "0.5in"
                }
            )
            
            await browser.close()
            print(f"[success] PDF created: {pdf_path}")
            return True
            
    except Exception as e:
        print(f"[error] Failed to convert {html_path.name}: {str(e)}")
        return False

async def batch_convert_folder(folder_path: pathlib.Path, pattern: str = "*.html"):
    """Convert all HTML files in a folder matching the pattern"""
    if not folder_path.exists() or not folder_path.is_dir():
        print(f"[error] Folder not found: {folder_path}")
        return
        
    html_files = list(folder_path.glob(pattern))
    if not html_files:
        print(f"[info] No HTML files found in: {folder_path}")
        return
        
    print(f"[info] Found {len(html_files)} HTML files")
    print(f"[info] Processing folder: {folder_path}")
    
    success_count = 0
    for html_file in html_files:
        success = await convert_single_html(html_file, folder_path)
        if success:
            success_count += 1
        print()  # Add spacing between files
        
    print(f"[summary] Successfully converted {success_count}/{len(html_files)} files")

def show_help():
    """Show usage instructions"""
    help_text = """
🚀 PORTABLE HTML TO PDF CONVERTER

USAGE OPTIONS:

1. SINGLE FILE:
   python batch_html_to_pdf.py filename.html
   python batch_html_to_pdf.py "C:\\path\\to\\file.html"

2. BATCH CONVERT CURRENT FOLDER:
   python batch_html_to_pdf.py .
   python batch_html_to_pdf.py --all

3. BATCH CONVERT SPECIFIC FOLDER:
   python batch_html_to_pdf.py "C:\\path\\to\\folder"

4. INTERACTIVE MODE:
   python batch_html_to_pdf.py
   (Will prompt for file/folder)

5. HELP:
   python batch_html_to_pdf.py --help

FEATURES:
- Letter format (8.5" x 11") with 0.5" margins
- Background graphics included
- Optimized for resumes and cover letters
- Handles complex CSS layouts
- Portable - works from any location

REQUIREMENTS:
- Python 3.7+
- playwright: pip install playwright
- Browser: playwright install chromium
"""
    print(help_text)

async def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        arg = sys.argv[1].strip().strip('"')
        
        if arg in ["--help", "-h", "help"]:
            show_help()
            return 0
            
        if arg in [".", "--all", "all"]:
            # Convert all HTML files in current directory
            await batch_convert_folder(pathlib.Path.cwd())
            return 0
            
        target_path = pathlib.Path(arg).expanduser()
        
        if not target_path.is_absolute():
            target_path = (pathlib.Path.cwd() / target_path).resolve()
            
        if target_path.is_file() and target_path.suffix.lower() == '.html':
            # Convert single file
            success = await convert_single_html(target_path)
            return 0 if success else 1
            
        elif target_path.is_dir():
            # Convert all HTML files in specified directory
            await batch_convert_folder(target_path)
            return 0
            
        else:
            print(f"[error] Invalid target: {arg}")
            print("Must be an HTML file or directory")
            return 1
    else:
        # Interactive mode
        try:
            inp = input("Enter HTML file or folder path (or 'help'): ").strip().strip('"')
            if inp.lower() in ['help', '--help']:
                show_help()
                return 0
            return await main_with_args([inp])
        except (KeyboardInterrupt, EOFError):
            print("\n[info] Cancelled by user")
            return 0

async def main_with_args(args):
    """Helper function to process arguments"""
    original_argv = sys.argv
    sys.argv = ['batch_html_to_pdf.py'] + args
    try:
        return await main()
    finally:
        sys.argv = original_argv

if __name__ == "__main__":
    try:
        code = asyncio.run(main())
        sys.exit(code or 0)
    except Exception as e:
        print("[fatal] Unexpected error:")
        traceback.print_exc()
        sys.exit(1)