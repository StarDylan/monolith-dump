import os
import re
import subprocess
import tldextract
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
import shutil
import sys

visited = set()

def sanitize_filename(url):
    from urllib.parse import urlparse
    import re

    parsed = urlparse(url)
    hostname = parsed.hostname or "unknown"
    path = parsed.path.strip("/")
    path = re.sub(r"[^\w\-]", "_", path)

    if not path:
        path = "index"

    safe_host = re.sub(r"[^\w\-]", "_", hostname)
    return f"{safe_host}__{path}.html"


def is_exact_subdomain_match(base_url, target_url):
    """
    Returns True if the hostname (subdomain + domain) of target_url exactly matches base_url.
    """
    base_host = urlparse(base_url).hostname
    target_host = urlparse(target_url).hostname

    return base_host == target_host

def is_allowed_target(target_url, start_urls):
    return any(is_exact_subdomain_match(base, target_url) for base in start_urls)


def rewrite_internal_links(filepath, base_url):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
    except Exception as e:
        print(f"ERROR: Failed to open {filepath} for link rewriting: {e}")
        return

    for tag in soup.find_all("a", href=True):
        original_href = tag["href"]
        full_url = urljoin(base_url, original_href)
        if is_exact_subdomain_match(base_url, full_url):
            tag["href"] = sanitize_filename(full_url)

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(str(soup))
    except Exception as e:
        print(f"ERROR: Failed to write updated links to {filepath}: {e}")


def get_links(html, base_url, start_urls):
    soup = BeautifulSoup(html, 'html.parser')
    links = set()
    for tag in soup.find_all('a', href=True):
        href = tag['href']
        full_url = urljoin(base_url, href)
        if full_url.startswith("http") and is_allowed_target(full_url, start_urls):
            links.add(full_url)
    return links

def fetch_and_save(url, output_dir, start_urls):
    if url in visited:
        return
    visited.add(url)

    filename = sanitize_filename(url)
    filepath = os.path.join(output_dir, filename)

    if not os.path.exists(filepath):
        try:
            print(f"SAVE: {url} -> {filename}")
            with open(filepath, "wb") as f:
                subprocess.run(["monolith", url], stdout=f, stderr=subprocess.DEVNULL)
        except Exception as e:
            print(f"ERROR: Failed to save {url}: {e}")
            return
    else:
        print(f"[SKIP] {url} already saved as {filename}")

    rewrite_internal_links(filepath, url)

    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        links = get_links(r.text, url, start_urls)
        for link in links:
            fetch_and_save(link, output_dir, start_urls)
    except Exception as e:
        print(f"ERROR: Failed to parse {url}: {e}")


def check_monolith_installed():
    """Check if 'monolith' is available in system PATH."""
    if shutil.which("monolith") is None:
        print("⚠️  ERROR: 'monolith' is not installed or not in your PATH.")
        print("   → Install it with:")
        print("     - Debian/Ubuntu: sudo apt install monolith")
        print("     - macOS (Homebrew): brew install monolith")
        print("     - Or: cargo install monolith")
        sys.exit(1)

def write_root_index(start_urls, output_dir):
    """
    Creates a file __index.html with links to the local copies of the start URLs.
    """
    lines = [
        "<!DOCTYPE html>",
        "<html>",
        "<head>",
        "  <meta charset='UTF-8'>",
        "  <title>📚 Monolith Root Index</title>",
        "  <style>",
        "    body { font-family: sans-serif; padding: 2rem; background: #f7f7f7; }",
        "    h1 { font-size: 1.5rem; }",
        "    ul { list-style: none; padding: 0; }",
        "    li { margin-bottom: 1rem; }",
        "    a { text-decoration: none; color: #007acc; font-weight: bold; }",
        "    a:hover { text-decoration: underline; }",
        "  </style>",
        "</head>",
        "<body>",
        "  <h1>📚 Start Pages</h1>",
        "  <ul>"
    ]

    for url in start_urls:
        filename = sanitize_filename(url)
        lines.append(f'    <li><a href="{filename}">{url}</a></li>')

    lines += [
        "  </ul>",
        "</body>",
        "</html>"
    ]

    index_path = os.path.join(output_dir, "__index.html")
    try:
        with open(index_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"[INDEX] Wrote root index to {index_path}")
    except Exception as e:
        print(f"[ERROR] Failed to write index file: {e}")

def main():
    check_monolith_installed()
    input_urls = input("Enter one or more URLs (comma-separated): ").strip()
    start_urls = [url.strip() for url in input_urls.split(",") if url.strip()]

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    for url in start_urls:
        print(f"START: Crawling from: {url}")
        fetch_and_save(url, output_dir, start_urls)

    write_root_index(start_urls, output_dir)

if __name__ == "__main__":
    main()
