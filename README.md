# ⚡ Lumina — Passive Reconnaissance Tool

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Stars](https://img.shields.io/github/stars/yourusername/lumina?style=flat-square)

> A fully passive OSINT reconnaissance tool for domains — zero requests to the target server.

Lumina collects data exclusively from third-party public sources, making it completely safe and undetectable for security researchers, penetration testers, and bug bounty hunters.

## 🔍 Features

- **Subdomain Enumeration** — via crt.sh Certificate Transparency logs
- **Wayback Machine** — historical URLs and endpoints
- **GitHub Leaks** — search for exposed secrets, tokens, and passwords
- **Shodan** — open ports, hosts, and infrastructure info
- **Beautiful HTML Report** — dark theme, clean UI

## 📸 Preview

![Lumina banner](report_example.jpg)

## 🚀 Installation

```bash
git clone https://github.com/yourusername/lumina
cd lumina
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and add your API keys:

```
GITHUB_TOKEN=your_github_token
SHODAN_API_KEY=your_shodan_api_key
```

## ⚙️ Usage

```bash
# Basic scan
python main.py -d example.com

# Custom output file
python main.py -d example.com -o results.html

# Skip GitHub search
python main.py -d example.com --skip-github

# Skip Shodan search
python main.py -d example.com --skip-shodan
```

## 🔑 API Keys

| Service | Required | Free Plan | Link                                         |
| ------- | -------- | --------- | -------------------------------------------- |
| GitHub  | Yes      | ✅        | [tokens](https://github.com/settings/tokens) |
| Shodan  | Yes      | ✅        | [account](https://account.shodan.io)         |

## ⚠️ Disclaimer

This tool is intended for **legal use only** — authorized security testing, bug bounty programs, and OSINT research. The author is not responsible for any misuse.

## 📄 License

MIT License — free to use and modify.
