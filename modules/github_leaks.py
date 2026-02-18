import httpx
from dotenv import load_dotenv
import os

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


async def search_github(domain: str):
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }

    queries = [
        f'"{domain}" password',
        f'"{domain}" api_key',
        f'"{domain}" secret',
        f'"{domain}" token',
    ]

    results = []

    async with httpx.AsyncClient(timeout=15) as client:
        for q in queries:
            try:
                r = await client.get(
                    "https://api.github.com/search/code",
                    params={"q": q, "per_page": 5},
                    headers=headers,
                )
                data = r.json()
                for item in data.get("items", []):
                    results.append(
                        {
                            "url": item["html_url"],
                            "repo": item["repository"]["full_name"],
                            "query": q,
                        }
                    )
                print(f"[+] GitHub '{q}' — {len(data.get('items', []))} results")
            except Exception as e:
                print(f"[-] GitHub error: {e}")

    return results
