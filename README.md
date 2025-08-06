# PassiveUrls

PassiveUrls is bug bounty recon tool that passively collects archived URLs for a target domain using the [Wayback Machine (archive.org)](https://archive.org/), then filters them using [uro](https://github.com/s0md3v/uro) to extract clean and unique URLs.

> ✅ No active scanning involved – stay stealthy and passive.

---

## ✨ Features

- Fetch URLs from the Wayback Machine (for current year or custom years)
- Filter and clean URLs using `uro`
- Save results per target in organized folders
- Optional printing of found URLs in the terminal
- Dependency auto-installer for `pipx` and `uro` if missing

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/YourUsername/PassiveUrls.git
cd PassiveUrls
pip3 install -r requirements.txt
```

## 🚀 Usage
```bash
python3 passive_urls.py -d domain.tld [options]
```

### Required Arguments

| Flag | Description |
|------|-------------|
| `-d` | Target domain (e.g., `example.com`) |

### Optional Flags

| Flag        | Description                                    |
|-------------|------------------------------------------------|
| `-po`       | Print the filtered URLs to the terminal output |

---
**Created by:** NakuTenshi

git clone https://github.com/YourUsername/PassiveUrls.git
cd PassiveUrls
