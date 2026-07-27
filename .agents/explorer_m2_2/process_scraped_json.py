import json

def main():
    try:
        with open("scraped_details_robust.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print("Error reading json:", e)
        return

    for site_name, site_data in data.items():
        if site_name != "google_sites":
            continue
            
        print(f"==================== {site_name} ====================")
        links = site_data.get("links", [])
        
        reconstructed = []
        for l in links:
            if isinstance(l, dict) and l.get("type") == "object":
                val = l.get("value", [])
                link_text = ""
                href = ""
                for pair in val:
                    if isinstance(pair, list) and len(pair) == 2:
                        k = pair[0]
                        v_obj = pair[1]
                        if isinstance(v_obj, dict):
                            v = v_obj.get("value", "")
                            if k == "text":
                                link_text = v
                            elif k == "href":
                                href = v
                if href:
                    reconstructed.append((link_text, href))
            elif isinstance(l, dict) and "text" in l and "href" in l:
                reconstructed.append((l["text"], l["href"]))
                
        print(f"Total reconstructed links: {len(reconstructed)}")
        for lt, h in reconstructed:
            if "dakahlya" in h.lower() or "leader" in lt.lower() or "teacher" in lt.lower() or "student" in lt.lower() or "contact" in lt.lower() or "bot" in lt.lower():
                print(f"  - {lt}: {h}")

if __name__ == "__main__":
    main()
