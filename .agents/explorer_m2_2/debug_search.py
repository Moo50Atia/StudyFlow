import asyncio
import nodriver as uc
import sys

async def main():
    browser = await uc.start()
    page = await browser.get("https://www.bing.com/search?q=Dakahlia+STEM+School")
    await page.wait(5)
    await page.save_screenshot("bing_debug.png")
    html = await page.evaluate("document.documentElement.innerHTML")
    with open("bing_debug.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Saved screenshot and HTML. Visible text length:", len(html))
    browser.stop()

if __name__ == "__main__":
    asyncio.run(main())
