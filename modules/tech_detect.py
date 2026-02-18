import httpx

SIGNATURES = {
    "WordPress": ["wp-content", "wp-includes"],
    "Nginx": ["nginx"],
    "Apache": ["Apache"],
    "Cloudflare": ["cloudflare", "__cfduid"],
    "React": ["react", "_next"],
    "jQuery": ["jquery"],
    "Bootstrap": ["bootstrap"],
    "Laravel": ["laravel_session"],
    "Django": ["csrfmiddlewaretoken"],
}

async def detect_tech(domain: str):
    detected = []
    try:
        async with httpx.AsyncClient(
            timeout=10,
            follow_redirects=True,
            headers={"User-Agent": "Mozilla/5.0"}
        ) as client:
            r = await client.get(f"https://{domain}")
            content = r.text.lower()
            headers = str(r.headers).lower()

            for tech, signatures in SIGNATURES.items():
                for sig in signatures:
                    if sig.lower() in content or sig.lower() in headers:
                        detected.append(tech)
                        break

            print(f"[+] Detected {len(detected)} technologies")
    except Exception as e:
        print(f"[-] Tech detect error: {e}")

    return detected