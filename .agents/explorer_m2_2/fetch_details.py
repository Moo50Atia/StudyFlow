import asyncio
import json
import nodriver as uc

async def fetch_urls(urls):
    browser = await uc.start()
    extracted_data = {}
    
    for label, url in urls.items():
        print(f"Fetching {label}: {url}")
        try:
            page = await browser.get(url)
            await page.wait(5)
            
            # Extract text
            text_res = await page.evaluate("""
                (() => {
                    try {
                        var bad = document.querySelectorAll('script, style, nav, footer, iframe');
                        for(var i=0; i<bad.length; i++) { bad[i].remove(); }
                        return document.body.innerText || document.body.textContent;
                    } catch(e) {
                        return "JS Error: " + e.message;
                    }
                })()
            """)
            
            # Extract links
            links_res = await page.evaluate("""
                (() => {
                    try {
                        var res = [];
                        var anchors = document.querySelectorAll('a');
                        for(var i=0; i<anchors.length; i++) {
                            var a = anchors[i];
                            var href = a.getAttribute('href');
                            var txt = a.textContent || a.innerText;
                            if (href) {
                                res.push({text: txt.trim(), href: href});
                            }
                        }
                        return res;
                    } catch(e) {
                        return [];
                    }
                })()
            """)
            
            # Safe check on types
            # nodriver evaluates return string, dict, list, int, float, bool, or ExceptionDetails
            text = text_res if isinstance(text_res, str) else str(text_res)
            links = links_res if isinstance(links_res, list) else []
            
            extracted_data[label] = {
                "url": url,
                "text": text,
                "links": links
            }
            print(f"Successfully fetched {label}, length of text: {len(text)}")
        except Exception as e:
            print(f"Error fetching {label} ({url}): {e}")
            
    browser.stop()
    
    with open("extracted_page_contents.json", "w", encoding="utf-8") as f:
        json.dump(extracted_data, f, indent=2, ensure_ascii=False)
    print("Done! Saved to extracted_page_contents.json")

if __name__ == "__main__":
    urls = {
        "netlify_site": "https://stemdk.netlify.app/",
        "google_sites": "https://sites.google.com/stemmaster.moe.edu.eg/stem/home/schools/dakahlya-stem-school",
        "directory_listing": "https://www.schoolandcollegelistings.com/EG/Gamasa/5284459437361129/Dakahlia-STEM-School"
    }
    asyncio.run(fetch_urls(urls))
