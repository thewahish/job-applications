import sys, pathlib, asyncio, traceback
from playwright.async_api import async_playwright, TimeoutError as PWTimeout

async def convert(target: str) -> int:
    print(f"[info] target = {target}")
    if target.lower().startswith(("http://", "https://")):
        url = target
        out_path = pathlib.Path.cwd() / "output.pdf"
    else:
        p = pathlib.Path(target).expanduser()
        if not p.is_absolute():
            p = (pathlib.Path.cwd() / p).resolve()
        print(f"[info] resolved input = {p}")
        if not p.exists():
            print(f"[error] file not found: {p}")
            return 2
        url = p.as_uri()
        out_path = p.with_suffix(".pdf")

    print(f"[info] url = {url}")
    print(f"[info] output = {out_path}")

    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        page = await browser.new_page()
        try:
            await page.goto(url, wait_until="networkidle", timeout=60000)
        except PWTimeout:
            print("[warn] networkidle timed out at 60s. Trying 'load'…")
            await page.goto(url, wait_until="load", timeout=60000)
        # Optional: honor CSS page size if present, else default A4
        try:
            await page.pdf(
                path=str(out_path),
                print_background=True,
                prefer_css_page_size=True,
                format="A4"
            )
        finally:
            await browser.close()

    print(f"[ok] PDF saved: {out_path}")
    return 0

async def main():
    if len(sys.argv) < 2:
        inp = input("Enter HTML file name (or URL): ").strip().strip('"')
    else:
        inp = sys.argv[1].strip().strip('"')
    try:
        code = await convert(inp)
    except Exception as e:
        print("[fatal] Unexpected error:")
        traceback.print_exc()
        code = 1
    raise SystemExit(code)

if __name__ == "__main__":
    asyncio.run(main())
