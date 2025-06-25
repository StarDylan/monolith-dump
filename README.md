# Monolith Recursive Archiver

This is a quick and dirty script that recursively crawls pages from a given starting URL (or list of URLs) and saves each one using monolith — producing standalone .html files with embedded assets for full offline viewing.

Links between pages are rewritten to reference local .html files, making the saved dump browsable like a real site.

## ⚙️ Requirements

- Python 3.8+ (preferably with `uv`)

- [monolith](https://github.com/Y2Z/monolith) installed and on your `$PATH`

Install Python deps:

```
uv sync
```

Install monolith:

```bash
# Ubuntu/Debian

sudo apt install monolith

# macOS

brew install monolith

# Or via Rust

cargo install monolith
```

## 🚀 Usage

python recursive_monolith_downloader.py

You'll be prompted:

```
Enter one or more URLs (comma-separated): https://blog.example.com, https://docs.example.com
```

The script will:

- Crawl each page on the same subdomain.

- Save them using monolith as standalone .html files.

- Rewrite internal `<a href>` links to point to the local files.

- Store all output in the monolith_dump/ directory.

## Examples

Save a tech blog:

Enter one or more URLs (comma-separated): https://blog.rust-lang.org

Save your own hosted wiki:

Enter one or more URLs (comma-separated): https://wiki.internal.example.com

🔧 Caveats

- Only follows links on the exact same subdomain.

- No concurrent crawling.

- Doesn’t handle dynamic JS-generated links.

- Not optimized for performance

## About This Project

This was a fast, AI-assisted script written for personal use.
