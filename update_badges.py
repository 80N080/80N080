import requests
import re
from bs4 import BeautifulSoup

USERNAME = "eduard-platon.6f312b2b"
README_PATH = "README.md"
IMG_WIDTH = 50

headers = {
    "User-Agent": "Mozilla/5.0"
}

url = f"https://www.credly.com/users/{USERNAME}"

def fetch_page():
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code != 200:
            raise SystemExit(f"Credly error: {r.status_code}")
        return r.text
    except Exception as e:
        raise SystemExit(f"Request failed: {e}")

html = fetch_page()
soup = BeautifulSoup(html, "html.parser")

badges = []

# Credly usa spesso meta + card structure (può cambiare, quindi parsing difensivo)
for img in soup.find_all("img"):
    src = img.get("src", "")
    alt = img.get("alt", "")

    if "badge" in src or "badge" in alt.lower():
        parent_a = img.find_parent("a")
        if parent_a:
            link = parent_a.get("href", "")
            badges.append(
                f'<a href="{link}"><img src="{src}" width="{IMG_WIDTH}" alt="{alt}"/></a>'
            )

# fallback se parsing fallisce
if not badges:
    raise SystemExit("No badges found: Credly layout may have changed")

with open(README_PATH, "r") as f:
    content = f.read()

new_section = "\n".join(badges)

pattern = r"<!-- badges-start -->(.*?)<!-- badges-end -->"
replacement = f"<!-- badges-start -->\n{new_section}\n<!-- badges-end -->"

updated = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open(README_PATH, "w") as f:
    f.write(updated)

print(f"OK: aggiornati {len(badges)} badge")
