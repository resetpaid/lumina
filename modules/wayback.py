import httpx

async def get_wayback_urls(domain: str):
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(
                "http://web.archive.org/cdx/search/cdx",
                params={
                    "url": f"*.{domain}/*",
                    "output": "json",
                    "fl": "original",
                    "collapse": "urlkey",
                    "limit": "150"
                }
            )
            data = r.json()
            urls = [x[0] for x in data[1:]]
            print(f"[+] Wayback Machine found {len(urls)} URLs")
            return urls
    except Exception as e:
        print(f"[-] Wayback error: {e}")
        return []