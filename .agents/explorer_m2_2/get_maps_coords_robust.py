import asyncio
import nodriver as uc
import re

async def main():
    browser = await uc.start()
    page = await browser.get("https://www.google.com/maps/search/Dakahlia+STEM+High+School")
    print("Navigated. Waiting for search to resolve...")
    await page.wait(12)
    
    resolved_url = page.url
    print("Resolved URL type:", type(resolved_url))
    
    # Let's check if the URL contains coordinates
    coords = None
    match = re.search(r'@([0-9.-]+),([0-9.-]+)', resolved_url)
    if match:
        coords = (match.group(1), match.group(2))
    
    # If not in URL, we can try to extract from script tags or other elements
    # Sometimes it's inside href of links or meta tags
    meta_url = await page.evaluate("""
        (() => {
            var meta = document.querySelector('meta[property="og:url"]');
            return meta ? meta.getAttribute('content') : null;
        })()
    """)
    
    if meta_url and not coords:
        match = re.search(r'@([0-9.-]+),([0-9.-]+)', meta_url)
        if match:
            coords = (match.group(1), match.group(2))
            
    # We can also evaluate window.location.href
    loc = await page.evaluate("window.location.href")
    
    with open("maps_coords.txt", "w", encoding="utf-8") as f:
        f.write(f"Original URL: {resolved_url}\n")
        f.write(f"Meta URL: {meta_url}\n")
        f.write(f"Window Location: {loc}\n")
        f.write(f"Coordinates: {coords}\n")
        
    print("Done! Saved to maps_coords.txt")
    browser.stop()

if __name__ == "__main__":
    asyncio.run(main())
