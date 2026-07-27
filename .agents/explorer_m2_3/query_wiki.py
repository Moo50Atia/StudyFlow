import requests
import json

def query_wikipedia(search_term):
    print(f"Querying Wikipedia for: {search_term}")
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": search_term,
        "utf8": 1,
        "formatversion": 2
    }
    headers = {
        "User-Agent": "STEMSchoolExplorer/1.0 (info@example.com)"
    }
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            search_results = data.get("query", {}).get("search", [])
            output = []
            for r in search_results:
                title = r.get("title")
                snippet = r.get("snippet")
                pageid = r.get("pageid")
                output.append(f"Title: {title}\nPage ID: {pageid}\nSnippet: {snippet}\n")
            return "\n".join(output)
        else:
            return f"Failed with status: {response.status_code}"
    except Exception as e:
        return f"Error: {e}"

def main():
    terms = [
        "Dakahlia STEM School",
        "STEM Schools in Egypt",
        "Talkha STEM School",
        "Mansoura STEM School"
    ]
    results = {}
    for t in terms:
        res = query_wikipedia(t)
        results[t] = res
        
    with open('wiki_results.txt', 'w', encoding='utf-8') as f:
        for t, val in results.items():
            f.write(f"========================================\n")
            f.write(f"WIKI SEARCH: {t}\n")
            f.write(f"========================================\n")
            f.write(val)
            f.write("\n\n")
            
    print("Wiki queries finished. Saved to wiki_results.txt")

if __name__ == '__main__':
    main()
