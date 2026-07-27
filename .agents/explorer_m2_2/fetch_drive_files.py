import asyncio
import nodriver as uc
import json

async def main():
    browser = await uc.start()
    urls = {
        "leaders": "https://drive.google.com/open?id=1JB8vN4wX6WCLc-fxARAnGny6wWAuPdsC1xl_uGAI5p8",
        "teachers": "https://drive.google.com/open?id=1qGguiPequ-uR8Mzo3kz0POah3NPjfjiKahN3SsTkmDc",
        "students": "https://drive.google.com/open?id=1LqarZ8so8ZmobjuaVTsVMid4vNQn9YiNrFjB4IjNwHc"
    }
    
    scraped_drive = {}
    for name, url in urls.items():
        print(f"Navigating to Drive file for {name} ({url})...")
        try:
            page = await browser.get(url)
            await page.wait(10) # Google Drive might take time to load
            
            title = await page.evaluate("document.title")
            print(f"Title of {name}: {title}")
            
            # Save screenshot
            await page.save_screenshot(f"drive_{name}.png")
            print(f"Saved drive_{name}.png")
            
            # Extract text
            text = await page.evaluate("""
                (() => {
                    var el = document.body;
                    if (!el) return "No body element";
                    return el.innerText || el.textContent;
                })()
            """)
            
            scraped_drive[name] = {
                "url": url,
                "title": title,
                "text": text[:5000] # Limit to first 5000 characters
            }
            
        except Exception as e:
            print(f"Error loading {name}: {e}")
            
    browser.stop()
    
    with open("drive_data.json", "w", encoding="utf-8") as f:
        json.dump(scraped_drive, f, indent=2, ensure_ascii=False)
    print("Done! Saved to drive_data.json")

if __name__ == "__main__":
    asyncio.run(main())
