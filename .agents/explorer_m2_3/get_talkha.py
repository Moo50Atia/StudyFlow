import requests
import json

def get_wikipedia_page(title):
    print(f"Fetching Wikipedia page: {title}")
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "titles": title,
        "explaintext": 1,
        "formatversion": 2
    }
    headers = {
        "User-Agent": "STEMSchoolExplorer/1.0"
    }
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            pages = data.get("query", {}).get("pages", [])
            if pages:
                return pages[0].get("extract", "No extract found.")
            return "No pages found."
        else:
            return f"Failed with status: {response.status_code}"
    except Exception as e:
        return f"Error: {e}"

def main():
    content = get_wikipedia_page("Talkha")
    with open('talkha_wiki.txt', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Talkha wiki page saved to talkha_wiki.txt")

if __name__ == '__main__':
    main()
