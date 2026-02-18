import httpx
from dotenv import load_dotenv
import os

load_dotenv()
HUNTER_API_KEY = os.getenv("HUNTER_API_KEY")

async def find_emails(domain: str):
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(
                "https://api.hunter.io/v2/domain-search",
                params={
                    "domain": domain,
                    "api_key": HUNTER_API_KEY,
                    "limit": 20
                }
            )
            data = r.json()
            emails = data.get("data", {}).get("emails", [])
            result = [{
                "email": e["value"],
                "type": e.get("type", "N/A"),
                "confidence": e.get("confidence", 0)
            } for e in emails]
            print(f"[+] Hunter.io found {len(result)} emails")
            return result
    except Exception as e:
        print(f"[-] Hunter.io error: {e}")
        return []