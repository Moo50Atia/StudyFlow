import requests
import json

def search_wikidata(search_term):
    print(f"Searching Wikidata for: {search_term}")
    url = "https://www.wikidata.org/w/api.php"
    params = {
        "action": "wbsearchentities",
        "format": "json",
        "search": search_term,
        "language": "en"
    }
    headers = {
        "User-Agent": "STEMSchoolExplorer/1.0"
    }
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            search_results = data.get("search", [])
            output = []
            for r in search_results:
                q_id = r.get("id")
                label = r.get("label")
                desc = r.get("description")
                output.append(f"Q-ID: {q_id}\nLabel: {label}\nDescription: {desc}\n")
            return "\n".join(output)
        else:
            return f"Failed with status: {response.status_code}"
    except Exception as e:
        return f"Error: {e}"

def main():
    terms = [
        "Dakahlia STEM",
        "Talkha STEM",
        "Mansoura STEM",
        "STEM School Egypt"
    ]
    results = {}
    for t in terms:
        res = search_wikidata(t)
        results[t] = res
        
    with open('wikidata_results.txt', 'w', encoding='utf-8') as f:
        for t, val in results.items():
            f.write(f"========================================\n")
            f.write(f"WIKIDATA SEARCH: {t}\n")
            f.write(f"========================================\n")
            f.write(val)
            f.write("\n\n")
            
    print("Wikidata queries finished. Saved to wikidata_results.txt")

if __name__ == '__main__':
    main()
