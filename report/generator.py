from jinja2 import Environment, FileSystemLoader
import os
from datetime import datetime

def generate_report(results: dict, output: str):
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