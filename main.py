import asyncio
import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from modules.subdomains import get_subdomains
from modules.wayback import get_wayback_urls
from modules.github_leaks import search_github
from modules.shodan import search_shodan
from modules.dns_lookup import dns_lookup
from modules.emails import find_emails
from modules.tech_detect import detect_tech
from report.generator import generate_report

console = Console()

BANNER = """
[bold cyan]
 ██╗     ██╗   ██╗███╗   ███╗██╗███╗   ██╗ █████╗ 
 ██║     ██║   ██║████╗ ████║██║████╗  ██║██╔══██╗
 ██║     ██║   ██║██╔████╔██║██║██╔██╗ ██║███████║
 ██║     ██║   ██║██║╚██╔╝██║██║██║╚██╗██║██╔══██║
 ███████╗╚██████╔╝██║ ╚═╝ ██║██║██║ ╚████║██║  ██║
 ╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝
[/bold cyan]
[bold white]        Passive Reconnaissance Tool v1.0[/bold white]
[dim]        github.com/surfruit/lumina[/dim]
"""

@click.command()
@click.option('--domain', '-d', required=True, help='Target domain (e.g. example.com)')
@click.option('--output', '-o', default='report.html', help='Output file name')
@click.option('--skip-github', is_flag=True, help='Skip GitHub search')
@click.option('--skip-shodan', is_flag=True, help='Skip Shodan search')
def main(domain, output, skip_github, skip_shodan):
    console.print(BANNER)
    console.print(Panel(f"[bold green]Target:[/bold green] {domain}", expand=False))

    results = {
        "domain": domain,
        "subdomains": [],
        "wayback_urls": [],
        "github_leaks": [],
        "shodan": {"subdomains": [], "hosts": []},
        "dns": {},
        "emails": [],
        "technologies": []
    }

    async def run():
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:

            task1 = progress.add_task("[cyan]Searching subdomains (crt.sh)...", total=None)
            results["subdomains"] = await get_subdomains(domain)
            progress.update(task1, description=f"[green]✓ Subdomains: {len(results['subdomains'])} found")
            progress.stop_task(task1)

            task2 = progress.add_task("[cyan]Searching Wayback Machine...", total=None)
            results["wayback_urls"] = await get_wayback_urls(domain)
            progress.update(task2, description=f"[green]✓ Wayback URLs: {len(results['wayback_urls'])} found")
            progress.stop_task(task2)

            if not skip_github:
                task3 = progress.add_task("[cyan]Searching GitHub leaks...", total=None)
                results["github_leaks"] = await search_github(domain)
                progress.update(task3, description=f"[green]✓ GitHub leaks: {len(results['github_leaks'])} found")
                progress.stop_task(task3)

            if not skip_shodan:
                task4 = progress.add_task("[cyan]Querying Shodan...", total=None)
                results["shodan"] = await search_shodan(domain)
                progress.update(task4, description=f"[green]✓ Shodan: {len(results['shodan']['hosts'])} hosts found")
                progress.stop_task(task4)

            task5 = progress.add_task("[cyan]DNS lookup...", total=None)
            results["dns"] = await dns_lookup(domain)
            progress.update(task5, description=f"[green]✓ DNS records found")
            progress.stop_task(task5)

            task6 = progress.add_task("[cyan]Harvesting emails...", total=None)
            results["emails"] = await find_emails(domain)
            progress.update(task6, description=f"[green]✓ Emails: {len(results['emails'])} found")
            progress.stop_task(task6)

            task7 = progress.add_task("[cyan]Detecting technologies...", total=None)
            results["technologies"] = await detect_tech(domain)
            progress.update(task7, description=f"[green]✓ Technologies: {len(results['technologies'])} found")
            progress.stop_task(task7)

    asyncio.run(run())

    console.print("\n[cyan]Generating HTML report...[/cyan]")
    generate_report(results, output)
    console.print(f"\n[bold green]✓ Done! Report saved: {output}[/bold green]")

if __name__ == '__main__':
    main()