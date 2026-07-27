import asyncio
import nodriver as uc

async def main():
    browser = await uc.start()
    page = await browser.get("https://www.google.com/maps/search/Dakahlia+STEM+High+School")
    await page.wait(8)
    
    # Get current URL which should contain coordinates once resolved
    current_url = page.url
    print("Resolved Maps URL:", current_url)
    
    title = await page.evaluate("document.title")
    print("Page Title:", title)
    
    await page.save_screenshot("maps_result.png")
    
    browser.stop()

if __name__ == "__main__":
    asyncio.run(main())
