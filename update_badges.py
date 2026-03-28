import requests
import re

USERNAME = "eduard-platon.6f312b2b" 
README_PATH = "README.md"
IMG_WIDTH = 50 

# Recupera dati dei badge
url = f"https://www.credly.com/users/{USERNAME}/badges.json"
r = requests.get(url)
if r.status_code != 200:
    raise SystemExit(f"Errore nel recupero dei badge: {r.status_code}")

data = r.json().get("data", [])
badges = []

for b in data:
    name = b["badge_template"]["name"]
    img = b["badge_template"]["image"]["url"]
    badge_id = b["id"]
    link = f"https://www.credly.com/badges/{badge_id}"
    # Markdown HTML con larghezza fissa
    badges.append(f'<a href="{link}"><img src="{img}" width="{IMG_WIDTH}" alt="{name}"/></a>')

# Leggi il README e sostituisci la sezione
with open(README_PATH, "r") as f:
    content = f.read()

new_section = "\n".join(badges)
pattern = r"<!-- badges-start -->(.*?)<!-- badges-end -->"
replacement = f"<!-- badges-start -->\n{new_section}\n<!-- badges-end -->"
updated = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open(README_PATH, "w") as f:
    f.write(updated)

print(f"✅ Sezione badge aggiornata con larghezza {IMG_WIDTH}px!")
