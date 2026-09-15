import os

import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("GITHUB_TOKEN")
OWNER = os.getenv("GITHUB_OWNER")
REPO = os.getenv("GITHUB_REPO")

if not TOKEN:
    raise RuntimeError("GITHUB_TOKEN não encontrado no .env")

BASE_URL = f"https://api.github.com/repos/{OWNER}/{REPO}"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
}


def consultar_repositorio():
    response = requests.get(
        BASE_URL,
        headers=HEADERS,
        timeout=30,
    )

    response.raise_for_status()
    return response.json()


def consultar_commits(limite=10):
    response = requests.get(
        f"{BASE_URL}/commits",
        headers=HEADERS,
        params={"per_page": limite},
        timeout=30,
    )

    response.raise_for_status()
    return response.json()


def consultar_branches():
    response = requests.get(
        f"{BASE_URL}/branches",
        headers=HEADERS,
        timeout=30,
    )

    response.raise_for_status()
    return response.json()
