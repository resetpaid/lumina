# Contributing to Lumina

Thanks for your interest in contributing! 🎉

## How to contribute

1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Commit: `git commit -m "feat: add your feature"`
5. Push: `git push origin feature/your-feature`
6. Open a Pull Request

## Adding a new module

Each module lives in `modules/` and follows this pattern:

```python
import httpx

async def your_function(domain: str):
    results = []
    try:
        # your logic here
        pass
    except Exception as e:
        print(f"[-] Error: {e}")
    return results
```

## Reporting bugs

Open an issue with:

- Description of the bug
- Steps to reproduce
- Expected vs actual behavior

## Ideas for new modules

- VirusTotal integration
- SecurityTrails API
- WHOIS lookup
- Email harvesting
