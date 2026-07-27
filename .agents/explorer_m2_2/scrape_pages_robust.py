import asyncio
import json
import nodriver as uc

async def scrape():
    browser = await uc.start()
    urls = {
        "netlify": "https://stemdk.netlify.app/",
        "google_sites": "https://sites.google.com/stemmaster.moe.edu.eg/stem/home/schools/dakahlya-stem-school",
        "facebook": "https://www.facebook.com/STEMDakahlia/"
    }
    
    scraped_data = {}
    for name, url in urls.items():
        print(f"Scraping {name} ({url})...")
        try:
            page = await browser.get(url)
            # Wait up to 10 seconds for document.body to load
            for i in range(10):
                is_body_loaded = await page.evaluate("document.body !== null")
                if is_body_loaded:
                    break
                await asyncio.sleep(1)
                
            await page.wait(3) # Wait extra time for JS to run
            
            # Extract text and links using standard DOM methods
            text = await page.evaluate("""
                (() => {
                    var el = document.body;
                    if (!el) return "No body element";
                    // Clone body to avoid mutating actual page
                    var clone = el.cloneNode(true);
                    var bad = clone.querySelectorAll('script, style, nav, footer, iframe');
                    for (var i = 0; i < bad.length; i++) { bad[i].remove(); }
                    return clone.innerText || clone.textContent;
                })()
            """)
            
            links = await page.evaluate("""
                (() => {
                    var res = [];
                    var anchors = document.querySelectorAll('a');
                    for (var i = 0; i < anchors.length; i++) {
                        var a = anchors[i];
                        var href = a.getAttribute('href');
                        var txt = a.textContent || a.innerText;
                        if (href && !href.startsWith('javascript:')) {
                            res.push({text: txt.trim(), href: href});
                        }
                    }
                    return res;
                })()
            """)
            
            scraped_data[name] = {
                "url": url,
                "text": text,
                "links": links
            }
            print(f"Done scraping {name}. Text length: {len(text)}, links count: {len(links)}")
        except Exception as e:
            print(f"Error scraping {name}: {e}")
            
    browser.stop()
    
    with open("scraped_details_robust.json", "w", encoding="utf-8") as f:
        json.dump(scraped_data, f, indent=2, ensure_ascii=False)
    print("Saved all details to scraped_details_robust.json")

if __name__ == "__main__":
    asyncio.run(scrape())
