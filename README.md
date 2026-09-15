# Repo Monitor

Monitor de repositórios GitHub utilizando a GitHub REST API.

O projeto foi criado para acompanhar o estado de um repositório privado,
permitindo consultar informações do repositório, commits e branches.

## Funcionalidades atuais

- Autenticação na GitHub API
- Consulta de repositório privado
- Identificação da branch principal
- Consulta dos últimos commits da main
- Listagem dinâmica das branches existentes
- Identificação do último commit de cada branch

## Tecnologias

- Python 3.10
- uv
- GitHub REST API
- requests
- python-dotenv

## Estrutura

```text
repo_monitor/
├── src/
│   ├── monitor.py
│   └── monitor_branches.py
├── .env
├── .gitignore
├── .python-version
├── pyproject.toml
├── uv.lock
└── README.md
