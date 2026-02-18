import httpx


async def dns_lookup(domain: str):
    record_types = ["A", "MX", "NS", "TXT", "AAAA"]
    results = {}

    async with httpx.AsyncClient(timeout=10) as client:
        for record in record_types:
            try:
                r = await client.get(
                    "https://dns.google/resolve",
                    params={"name": domain, "type": record},
                )
                data = r.json()
                answers = data.get("Answer", [])
                results[record] = [a["data"] for a in answers]
                print(f"[+] DNS {record}: {len(answers)} records found")
            except Exception as e:
                print(f"[-] DNS {record} error: {e}")
                results[record] = []

    return results
