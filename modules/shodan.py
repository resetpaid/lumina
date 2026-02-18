import httpx
from dotenv import load_dotenv
import os

load_dotenv()
SHODAN_API_KEY = os.getenv("SHODAN_API_KEY")


async def search_shodan(domain: str):
    results = []

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(
                "https://api.shodan.io/dns/domain/{domain}".format(domain=domain),
                params={"key": SHODAN_API_KEY},
            )
            data = r.json()

            subdomains = data.get("subdomains", [])
            for sub in subdomains:
                results.append(f"{sub}.{domain}")

            print(f"[+] Shodan found {len(subdomains)} subdomains")

            # Також шукаємо хости
            r2 = await client.get(
                "https://api.shodan.io/shodan/host/search",
                params={
                    "key": SHODAN_API_KEY,
                    "query": f"hostname:{domain}",
                    "limit": 10,
                },
            )
            data2 = r2.json()
            hosts = data2.get("matches", [])

            host_info = []
            for h in hosts:
                host_info.append(
                    {
                        "ip": h.get("ip_str"),
                        "ports": h.get("port"),
                        "org": h.get("org", "N/A"),
                        "os": h.get("os", "N/A"),
                    }
                )

            print(f"[+] Shodan found {len(hosts)} hosts with {domain} in hostname")
            return {"subdomains": results, "hosts": host_info}

    except Exception as e:
        print(f"[-] Shodan error: {e}")
        return {"subdomains": [], "hosts": []}
