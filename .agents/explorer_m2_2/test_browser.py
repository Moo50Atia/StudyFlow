import asyncio
import nodriver as uc

async def main():
    print("Starting nodriver...")
    browser = await uc.start()
    print("Browser started. Navigating to google.com...")
    page = await browser.get("https://www.google.com")
    print("Navigated. Taking screenshot...")
    await page.save_screenshot("google.png")
    print("Screenshot saved. Page title:", await page.evaluate("document.title"))
    await browser.stop()

if __name__ == "__main__":
    asyncio.run(main())
