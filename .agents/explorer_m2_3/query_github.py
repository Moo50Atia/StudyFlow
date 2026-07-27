import requests
import json

def search_github(query):
    print(f"Searching GitHub for: {query}")
    url = f"https://api.github.com/search/repositories?q={query}"
    headers = {
        "User-Agent": "STEMSchoolExplorer/1.0",
        "Accept": "application/vnd.github.v3+json"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            items = data.get("items", [])
            output = []
            for item in items[:15]:
                name = item.get("name")
                desc = item.get("description")
                html_url = item.get("html_url")
                updated_at = item.get("updated_at")
                output.append(f"Repo: {name}\nURL: {html_url}\nDescription: {desc}\nUpdated: {updated_at}\n")
            return "\n".join(output)
        else:
            return f"Failed with status: {response.status_code}"
    except Exception as e:
        return f"Error: {e}"

def main():
    queries = [
        "Dakahlia STEM",
        "Talkha STEM",
        "Mansoura STEM"
    ]
    results = {}
    for q in queries:
        res = search_github(q)
        results[q] = res
        
    with open('github_results.txt', 'w', encoding='utf-8') as f:
        for q, text in results.items():
            f.write(f"========================================\n")
            f.write(f"GITHUB SEARCH: {q}\n")
            f.write(f"========================================\n")
            f.write(text)
            f.write("\n\n")
            
    print("GitHub search completed. Saved to github_results.txt")

if __name__ == '__main__':
    main()
