import requests
import json

def query_ddg(query):
    print(f"Querying DDG API for: {query}")
    url = f"https://api.duckduckgo.com/?q={query}&format=json"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"HTTP Status {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def main():
    queries = [
        "Dakahlia STEM School",
        "Talkha STEM School",
        "Mansoura STEM School"
    ]
    results = {}
    for q in queries:
        results[q] = query_ddg(q)
        
    with open('ddg_api_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4)
        
    print("DDG API query completed.")

if __name__ == '__main__':
    main()
