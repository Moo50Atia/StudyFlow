import json

def main():
    try:
        with open("arabic_search_results.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print("Error reading json:", e)
        return

    with open("parsed_arabic_results.txt", "w", encoding="utf-8") as out:
        for query, results in data.items():
            out.write(f"\n==================== {query} ====================\n")
            for idx, r in enumerate(results[:10]):
                title = r.get("title", "")
                url = r.get("url", "")
                snippet = r.get("snippet", "")
                out.write(f"[{idx}] {title}\n")
                out.write(f"    URL: {url}\n")
                out.write(f"    Snippet: {snippet}\n\n")
    print("Done! Saved to parsed_arabic_results.txt")

if __name__ == "__main__":
    main()
