import requests
import time
import difflib
import re
import trafilatura

URL_FILE = "private/urls.txt"
INTERVAL = 10  # seconds

def extract_main_content(html):
    return trafilatura.extract(html)

def load_urls(file_path):
    try:
        with open(file_path, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"❌ URL file not found: {file_path}")
        return []

def fetch_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        text = response.text
        text = normalize_content(text)
        return text
    except Exception as e:
        print(f"⚠️ Error fetching {url}: {e}")
        return None

def normalize_content(html):
    # return extract_main_content(html)  # Use trafilatura or readability
    content = extract_main_content(html)
    return content if content else ""

# Load URLs
URLS = load_urls(URL_FILE)

# Initialize
previous_content = {}
for url in URLS:
    content = fetch_content(url)
    if content:
        previous_content[url] = content
        print(f"📡 Monitoring started: {url}")
    else:
        previous_content[url] = ""

while True:
    time.sleep(INTERVAL)
    for url in URLS:
        new_content = fetch_content(url)
        old_content = previous_content.get(url, "")

        if new_content and new_content != old_content:
            print(f"\n🔔 Change detected at {url}")
            diff = difflib.unified_diff(
                old_content.splitlines(),
                new_content.splitlines(),
                fromfile='before',
                tofile='after',
                lineterm=''
            )
            print("\n".join(diff))
            previous_content[url] = new_content
