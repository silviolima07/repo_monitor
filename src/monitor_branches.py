import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("GITHUB_TOKEN")
OWNER = os.getenv("GITHUB_OWNER")
REPO = os.getenv("GITHUB_REPO")

BASE_URL = f"https://api.github.com/repos/{OWNER}/{REPO}"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
}


def consultar_branches():
    url = f"{BASE_URL}/branches"

    response = requests.get(
        url,
        headers=headers,
        timeout=30,
    )

    response.raise_for_status()
    return response.json()


branches = consultar_branches()

print("\n=== BRANCHES DO REPOSITÓRIO ===")
print(f"Total: {len(branches)}\n")

for branch in branches:
    nome = branch["name"]
    sha = branch["commit"]["sha"][:7]

    print(f"Branch: {nome}")
    print(f"Último commit: {sha}")
    print("-" * 40)
