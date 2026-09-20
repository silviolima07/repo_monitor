import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("GITHUB_TOKEN")
OWNER = os.getenv("GITHUB_OWNER")
REPO = os.getenv("GITHUB_REPO")

if not TOKEN:
    raise RuntimeError("GITHUB_TOKEN não encontrado no .env")

if not OWNER:
    raise RuntimeError("GITHUB_OWNER não encontrado no .env")

if not REPO:
    raise RuntimeError("GITHUB_REPO não encontrado no .env")


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


def consultar_commits(limite=10, branch=None):
    params = {
        "per_page": limite,
    }

    if branch:
        params["sha"] = branch

    response = requests.get(
        f"{BASE_URL}/commits",
        headers=HEADERS,
        params=params,
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


def consultar_pulls():
    response = requests.get(
        f"{BASE_URL}/pulls",
        headers=HEADERS,
        params={
            "state": "open",
            "per_page": 100,
        },
        timeout=30,
    )

    response.raise_for_status()
    return response.json()


def consultar_issues():
    response = requests.get(
        f"{BASE_URL}/issues",
        headers=HEADERS,
        params={
            "state": "open",
            "per_page": 100,
        },
        timeout=30,
    )

    response.raise_for_status()

    dados = response.json()

    # A API /issues também retorna Pull Requests.
    # Mantemos somente issues reais.
    return [
        issue
        for issue in dados
        if "pull_request" not in issue
    ]
