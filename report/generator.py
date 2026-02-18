from jinja2 import Environment, FileSystemLoader
import os
import json
from datetime import datetime

def generate_report(results: dict, output: str):
    # HTML report
    env = Environment(
        loader=FileSystemLoader(
            os.path.join(os.path.dirname(__file__))
        )
    )

    template = env.get_template("template.html")

    html = template.render(
        domain=results["domain"],
        subdomains=results["subdomains"],
        wayback_urls=results["wayback_urls"],
        github_leaks=results["github_leaks"],
        shodan_subdomains=results["shodan"]["subdomains"],
        shodan_hosts=results["shodan"]["hosts"],
        dns=results["dns"],
        emails=results["emails"],
        technologies=results["technologies"],
        whois=results["whois"],
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        total_subdomains=len(results["subdomains"]),
        total_urls=len(results["wayback_urls"]),
        total_leaks=len(results["github_leaks"]),
        total_hosts=len(results["shodan"]["hosts"]),
        total_emails=len(results["emails"]),
        total_techs=len(results["technologies"])
    )

    with open(output, "w", encoding="utf-8") as f:
        f.write(html)

    # JSON export
    json_output = output.replace(".html", ".json")
    json_data = {
        "meta": {
            "domain": results["domain"],
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_subdomains": len(results["subdomains"]),
            "total_urls": len(results["wayback_urls"]),
            "total_leaks": len(results["github_leaks"]),
            "total_hosts": len(results["shodan"]["hosts"]),
            "total_emails": len(results["emails"]),
            "total_techs": len(results["technologies"])
        },
        "subdomains": results["subdomains"],
        "wayback_urls": results["wayback_urls"],
        "github_leaks": results["github_leaks"],
        "shodan": results["shodan"],
        "dns": results["dns"],
        "emails": results["emails"],
        "technologies": results["technologies"],
        "whois": results["whois"]
    }

    with open(json_output, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)

    print(f"[+] JSON report saved: {json_output}")