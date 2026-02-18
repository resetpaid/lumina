import whois


async def whois_lookup(domain: str):
    try:
        w = whois.whois(domain)
        result = {
            "registrar": w.registrar or "N/A",
            "creation_date": str(
                w.creation_date[0]
                if isinstance(w.creation_date, list)
                else w.creation_date
            )
            or "N/A",
            "expiration_date": str(
                w.expiration_date[0]
                if isinstance(w.expiration_date, list)
                else w.expiration_date
            )
            or "N/A",
            "updated_date": str(
                w.updated_date[0]
                if isinstance(w.updated_date, list)
                else w.updated_date
            )
            or "N/A",
            "name_servers": w.name_servers or [],
            "country": w.country or "N/A",
            "org": w.org or "N/A",
        }
        print(f"[+] WHOIS: registrar — {result['registrar']}")
        return result
    except Exception as e:
        print(f"[-] WHOIS error: {e}")
        return {}
