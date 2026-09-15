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


def consultar_repositorio():
    response = requests.get(BASE_URL, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()


def consultar_commits():
    url = f"{BASE_URL}/commits"

    response = requests.get(
        url,
        headers=headers,
        params={"per_page": 10},
        timeout=30,
    )

    response.raise_for_status()
    return response.json()


repo = consultar_repositorio()

print("\n=== REPOSITÓRIO ===")
print(f"Nome: {repo['full_name']}")
print(f"Branch principal: {repo['default_branch']}")
print(f"Privado: {repo['private']}")

commits = consultar_commits()

print("\n=== ÚLTIMOS COMMITS ===")

for commit in commits:
    sha = commit["sha"][:7]
    mensagem = commit["commit"]["message"].split("\n")[0]
    autor = commit["commit"]["author"]["name"]
    data = commit["commit"]["author"]["date"]

    print(f"{sha} | {autor} | {data}")
    print(f"  {mensagem}")
