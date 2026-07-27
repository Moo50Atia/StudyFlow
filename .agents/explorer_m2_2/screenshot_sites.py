import asyncio
import nodriver as uc

async def main():
    browser = await uc.start()
    urls = {
        "netlify": "https://stemdk.netlify.app/",
        "google_sites": "https://sites.google.com/stemmaster.moe.edu.eg/stem/home/schools/dakahlya-stem-school",
        "directory": "https://www.schoolandcollegelistings.com/EG/Gamasa/5284459437361129/Dakahlia-STEM-School",
        "facebook": "https://www.facebook.com/STEMDakahlia/"
    }
    
    for name, url in urls.items():
        print(f"Navigating to {name}...")
        try:
            page = await browser.get(url)
            await page.wait(7)
            title = await page.evaluate("document.title")
            print(f"Title of {name}: {title}")
            await page.save_screenshot(f"{name}_screenshot.png")
            print(f"Saved {name}_screenshot.png")
        except Exception as e:
            print(f"Error on {name}: {e}")
            
    browser.stop()

if __name__ == "__main__":
    asyncio.run(main())
