# Repo Monitor

Monitor de repositórios privados do GitHub com interface via Telegram.

O projeto consulta a GitHub REST API para acompanhar o estado de um repositório, seus commits e branches, permitindo que integrantes do projeto consultem essas informações através de um bot no Telegram.

## Arquitetura

```text
Usuário
   |
   v
Telegram
   |
   v
RepoMonitor_bot
   |
   v
bot_repo_monitor.py
   |
   v
github_api.py
   |
   v
GitHub REST API
   |
   v
Repositório monitorado
```

O bot possui somente função de consulta. Ele não altera arquivos, branches, commits ou configurações do repositório monitorado.

## Funcionalidades atuais

- Autenticação em repositório privado do GitHub
- Consulta de informações gerais do repositório
- Identificação da branch principal
- Consulta dos últimos commits da `main`
- Identificação de autor, data, mensagem e SHA dos commits
- Descoberta dinâmica das branches existentes
- Consulta pelo Telegram
- Comando `/start`
- Comando `/status`
- Comando `/branches`

## Estrutura do projeto

```text
repo_monitor/
├── docs/
│   └── RELATORIO_REPO_MONITOR.md
├── src/
│   ├── github_api.py
│   ├── monitor.py
│   ├── monitor_branches.py
│   └── bot_repo_monitor.py
├── .env
├── .gitignore
├── .python-version
├── pyproject.toml
├── uv.lock
└── README.md
```

### Responsabilidade dos módulos

**`github_api.py`**

Centraliza as funções responsáveis pela comunicação com a GitHub REST API.

Atualmente fornece consultas de:

- repositório;
- commits;
- branches.

**`monitor.py`**

Executa consultas pelo terminal e apresenta informações gerais do repositório e commits recentes.

**`monitor_branches.py`**

Consulta dinamicamente as branches existentes no repositório.

**`bot_repo_monitor.py`**

Implementa a interface Telegram e utiliza as funções de `github_api.py` para consultar o GitHub.

## Requisitos

- Python 3.10
- uv
- Git
- Conta GitHub com acesso ao repositório monitorado
- Fine-grained Personal Access Token do GitHub
- Bot criado no Telegram através do BotFather

## Instalação

Clone o repositório:

```bash
git clone git@github.com:silviolima07/repo_monitor.git
cd repo_monitor
```

Sincronize o ambiente e instale as dependências:

```bash
uv sync
```

O projeto utiliza, entre outras, as bibliotecas:

- `requests`
- `python-dotenv`
- `python-telegram-bot`

## Configuração do GitHub Token

Como o repositório monitorado é privado, cada usuário deve possuir autorização para acessá-lo.

Foi utilizado um **Fine-grained Personal Access Token** com acesso somente ao repositório necessário.

Permissões utilizadas em modo somente leitura:

- Actions
- Commit statuses
- Contents
- Issues
- Metadata
- Pull requests

Não devem ser concedidas permissões de escrita se o objetivo for apenas monitoramento.

## Configuração do Telegram

Crie um bot utilizando o BotFather no Telegram.

O bot utilizado durante o desenvolvimento foi denominado:

```text
RepoMonitor_bot
```

O BotFather fornecerá um token exclusivo para o bot.

Esse token nunca deve ser colocado diretamente no código-fonte.

## Arquivo .env

Crie um arquivo `.env` na raiz do projeto:

```env
GITHUB_TOKEN=seu_token_github
GITHUB_OWNER=nome_da_organizacao
GITHUB_REPO=nome_do_repositorio
TELEGRAM_TOKEN=seu_token_telegram
```

O `.env` contém informações sensíveis e **não deve ser versionado no Git**.

Antes de realizar commits, confirme:

```bash
git status
```

e verifique que `.env` não aparece entre os arquivos versionados.

## Execução pelo terminal

Monitor geral:

```bash
uv run python src/monitor.py
```

Monitor de branches:

```bash
uv run python src/monitor_branches.py
```

## Execução do bot

Execute:

```bash
uv run python src/bot_repo_monitor.py
```

Enquanto o processo estiver ativo, o bot ficará aguardando mensagens do Telegram através de polling.

## Comandos do Telegram

### /start

Verifica se o bot está ativo e apresenta os comandos disponíveis.

### /status

Consulta o GitHub e retorna informações reais do repositório, incluindo:

- nome do repositório;
- branch principal;
- issues abertas;
- último commit;
- autor;
- data;
- mensagem.

### /branches

Consulta dinamicamente as branches existentes no repositório e apresenta o último commit conhecido de cada branch.

Não é necessário cadastrar os nomes das branches manualmente.

## Estratégia de branches

O grupo definiu que o desenvolvimento será realizado utilizando branches por tarefa ou por pessoa.

Exemplo:

```text
main
 |
 +-- feature/tarefa-a
 |
 +-- feature/tarefa-b
 |
 +-- pessoa/tarefa-c
```

Por esse motivo, monitorar somente a `main` não é suficiente.

Uma pessoa pode possuir commits em sua branch que ainda não foram integrados à `main`.

O `repo_monitor` deverá evoluir para acompanhar também essa atividade.

## Próximas etapas

- Mostrar autor, data e mensagem do último commit de cada branch
- Consultar commits por branch
- Comparar branches com a `main`
- Mostrar commits à frente e atrás da `main`
- Monitorar Pull Requests
- Monitorar GitHub Actions
- Consolidar atividade dos integrantes
- Melhorar os comandos e respostas do Telegram
- Criar tratamento centralizado de erros
- Executar o bot como serviço no Ubuntu

## Segurança

Nunca versionar:

```text
.env
```

Nunca colocar diretamente no código:

```text
GitHub Token
Telegram Token
```

Cada usuário que clonar o projeto deve configurar suas próprias credenciais e possuir as permissões necessárias para acessar o repositório privado.

## Documentação

O histórico detalhado da construção do projeto está disponível em:

```text
docs/RELATORIO_REPO_MONITOR.md
```
