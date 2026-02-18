import httpx


async def get_subdomains(domain: str):
    results = []

    # Source 1: crt.sh
    try:
        async with httpx.AsyncClient(
            timeout=15, headers={"User-Agent": "Mozilla/5.0"}
        ) as client:
            r = await client.get(f"https://crt.sh/?q=%.{domain}&output=json")
            data = r.json()
            subs = list(set([x["name_value"] for x in data]))
            results.extend(subs)
            print(f"[+] crt.sh found {len(subs)} subdomains")
    except Exception as e:
        print(f"[-] crt.sh error: {e}")

    # Source 2: HackerTarget (fallback)
    try:
        async with httpx.AsyncClient(
            timeout=15, headers={"User-Agent": "Mozilla/5.0"}
        ) as client:
            r = await client.get(f"https://api.hackertarget.com/hostsearch/?q={domain}")
            if "error" not in r.text.lower() and "API count" not in r.text:
                lines = r.text.strip().split("\n")
                subs = [line.split(",")[0] for line in lines if line]
                results.extend(subs)
                print(f"[+] HackerTarget found {len(subs)} subdomains")
    except Exception as e:
        print(f"[-] HackerTarget error: {e}")

    # Source 3: AlienVault OTX
    try:
        async with httpx.AsyncClient(
            timeout=15, headers={"User-Agent": "Mozilla/5.0"}
        ) as client:
            r = await client.get(
                f"https://otx.alienvault.com/api/v1/indicators/domain/{domain}/passive_dns"
            )
            data = r.json()
            subs = list(
                set(
                    [
                        x["hostname"]
                        for x in data.get("passive_dns", [])
                        if domain in x.get("hostname", "")
                    ]
                )
            )
            results.extend(subs)
            print(f"[+] AlienVault found {len(subs)} subdomains")
    except Exception as e:
        print(f"[-] AlienVault error: {e}")

    return list(set(results))
