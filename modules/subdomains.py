import httpx

async def get_subdomains(domain: str):
    results = []
    
    try:
        async with httpx.AsyncClient(timeout=15, headers={"User-Agent": "Mozilla/5.0"}) as client:
            r = await client.get(
                f"https://crt.sh/?q=%.{domain}&output=json"
            )
            data = r.json()
            subs = list(set([x['name_value'] for x in data]))
            results.extend(subs)
            print(f"[+] crt.sh found {len(subs)} subdomains")
    except Exception as e:
        print(f"[-] crt.sh error: {e}")
    
    return list(set(results))