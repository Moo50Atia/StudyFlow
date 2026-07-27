import asyncio
import sys
import json
import nodriver as uc
from urllib.parse import quote_plus

async def search_bing(query, num_results=10):
    print(f"Searching Bing for: '{query}'")
    browser = await uc.start()
    url = f"https://www.bing.com/search?q={quote_plus(query)}"
    page = await browser.get(url)
    
    # Wait for the results to load
    await page.wait(2)
    
    # Extract results
    # We can evaluate js to find .b_algo elements
    js_code = """
    (async () => {
        let results = [];
        let items = document.querySelectorAll('li.b_algo');
        for (let item of items) {
            let titleEl = item.querySelector('h2 a');
            let snippetEl = item.querySelector('.b_caption p, .b_text');
            if (titleEl) {
                results.append({
                    title: titleEl.innerText,
                    url: titleEl.getAttribute('href'),
                    snippet: snippetEl ? snippetEl.innerText : ''
                });
            }
        }
        // If results is empty, try another selector
        if (results.length === 0) {
            let links = document.querySelectorAll('a');
            for (let link of links) {
                let href = link.getAttribute('href');
                if (href && href.startsWith('http') && !href.includes('bing.com') && !href.includes('microsoft.com')) {
                    results.append({
                        title: link.innerText,
                        url: href,
                        snippet: ''
                    });
                }
            }
        }
        return results;
    })()
    """
    # Wait, the evaluate method in nodriver takes js code. Let's make sure it doesn't fail.
    # Actually nodriver evaluate takes a js string.
    try:
        # In nodriver, page.evaluate runs code in the page context.
        # Let's write standard JS.
        results = await page.evaluate("""
            (() => {
                var res = [];
                var items = document.querySelectorAll('li.b_algo');
                for (var i = 0; i < items.length; i++) {
                    var item = items[i];
                    var titleEl = item.querySelector('h2 a');
                    var snippetEl = item.querySelector('.b_caption p, .b_algo_text, .b_caption, .b_text');
                    if (titleEl) {
                        res.push({
                            title: titleEl.textContent || titleEl.innerText,
                            url: titleEl.getAttribute('href'),
                            snippet: snippetEl ? snippetEl.textContent || snippetEl.innerText : ''
                        });
                    }
                }
                return res;
            })()
        """)
    except Exception as e:
        print(f"Error during evaluate: {e}")
        results = []
        
    print(f"Found {len(results)} results.")
    browser.stop()
    return results

async def fetch_page(url):
    print(f"Fetching URL: '{url}'")
    browser = await uc.start()
    try:
        page = await browser.get(url)
        await page.wait(4) # Wait for page to load
        
        # Get body text
        text = await page.evaluate("""
            (() => {
                // Remove scripts, styles, navs, footers to clean up
                var bad = document.querySelectorAll('script, style, nav, footer, iframe');
                for(var i=0; i<bad.length; i++) { bad[i].remove(); }
                return document.body.innerText || document.body.textContent;
            })()
        """)
        
        # Also grab any links
        links = await page.evaluate("""
            (() => {
                var res = [];
                var anchors = document.querySelectorAll('a');
                for(var i=0; i<anchors.length; i++) {
                    var a = anchors[i];
                    var href = a.getAttribute('href');
                    var text = a.textContent || a.innerText;
                    if (href && (href.startsWith('http') || href.includes('linkedin') || href.includes('facebook'))) {
                        res.push({text: text.trim(), href: href});
                    }
                }
                return res;
            })()
        """)
    except Exception as e:
        print(f"Error fetching page: {e}")
        text = ""
        links = []
        
    browser.stop()
    return text, links

async def main():
    if len(sys.argv) < 3:
        print("Usage: python search_engine.py search <query> OR python search_engine.py fetch <url>")
        return
        
    cmd = sys.argv[1]
    arg = " ".join(sys.argv[2:])
    
    if cmd == "search":
        res = await search_bing(arg)
        print(json.dumps(res, indent=2, ensure_ascii=False))
    elif cmd == "fetch":
        text, links = await fetch_page(arg)
        print("--- PAGE TEXT (TRUNCATED TO 3000 CHARS) ---")
        print(text[:3000])
        print("--- LINKS FOUND ---")
        print(json.dumps(links[:50], indent=2, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(main())
