# Repo Monitor --- Relatório de criação e primeiros monitoramentos

**Data:** 15/09/2026\
**Projeto:** `repo_monitor`

## 1. Objetivo

O `repo_monitor` foi criado como um projeto independente para consultar
e acompanhar o estado de um repositório GitHub utilizado por um grupo de
trabalho.

O repositório inicialmente monitorado é:

`Residencia-Time2/saude-publica-protocolos-clinicos`

O projeto de monitoramento fica separado tanto do repositório do grupo
quanto de outros projetos pessoais. A intenção é que o monitor seja
genérico e possa posteriormente ser reutilizado em outros repositórios.

O objetivo inicial é obter informações por meio da GitHub REST API sem
modificar o repositório monitorado.

## 2. Estratégia de monitoramento

O grupo definiu que o desenvolvimento será realizado em branches criadas
por tarefa ou por pessoa. Dessa forma, os commits realizados durante o
desenvolvimento não afetam imediatamente a branch `main`.

Isso levou à definição de dois primeiros tipos de monitoramento:

-   `monitor.py`: consulta informações gerais do repositório e os
    commits disponíveis na `main`.
-   `monitor_branches.py`: descobre dinamicamente as branches existentes
    no repositório.

No futuro, o monitor de branches poderá comparar cada branch com a
`main`, identificar atividade individual e acompanhar Pull Requests.

## 3. Criação do projeto

O repositório `repo_monitor` foi criado separadamente e clonado no
Ubuntu no diretório:

``` text
~/projetos/repo_monitor
```

A estrutura inicial foi criada utilizando `uv`:

``` bash
uv init
```

O comando inicializou o projeto Python com estrutura semelhante a:

``` text
repo_monitor/
├── .git/
├── .gitignore
├── .python-version
├── README.md
├── pyproject.toml
└── src/
```

O projeto está utilizando Python 3.10.

## 4. Gerenciamento do ambiente com uv

Foi escolhido o `uv` para gerenciamento do ambiente Python e das
dependências.

A instalação no Ubuntu foi feita com:

``` bash
sudo snap install astral-uv --classic
```

A versão verificada durante a configuração foi:

``` text
uv 0.12.6
```

Com `uv`, não é necessário ativar manualmente o ambiente virtual para
executar o projeto. Os comandos podem ser executados diretamente com
`uv run`.

Exemplo:

``` bash
uv run python src/monitor.py
```

As dependências iniciais utilizadas pelo projeto são:

-   `requests`
-   `python-dotenv`

Instalação:

``` bash
uv add requests python-dotenv
```

O `uv` gerencia o ambiente virtual `.venv`, o arquivo `pyproject.toml` e
o arquivo de lock das dependências.

## 5. Autenticação na GitHub API

Como o repositório monitorado é privado, as consultas à GitHub REST API
precisam ser autenticadas.

Para o primeiro MVP foi utilizado um **Fine-grained Personal Access
Token (PAT)**.

### 5.1 Configuração do token

No GitHub, foi criado um Fine-grained Personal Access Token com acesso
limitado ao repositório:

``` text
Residencia-Time2/saude-publica-protocolos-clinicos
```

Foi selecionada a opção de acesso somente ao repositório necessário,
evitando conceder acesso desnecessário a outros projetos.

### 5.2 Permissões

Foram configuradas permissões de repositório somente para leitura:

-   Actions
-   Commit statuses
-   Contents
-   Issues
-   Metadata
-   Pull requests

Não foram concedidas permissões de escrita ou administração.

Esse princípio é importante para o monitor: ele deve observar o projeto,
e não modificar seu conteúdo.

## 6. Proteção do token

O token não foi colocado diretamente no código-fonte.

Foi criado um arquivo `.env` na raiz do projeto:

``` env
GITHUB_TOKEN=seu_token_aqui
GITHUB_OWNER=Residencia-Time2
GITHUB_REPO=saude-publica-protocolos-clinicos
```

O `.env` está ignorado pelo Git através do `.gitignore`, impedindo que o
token seja enviado ao repositório.

Antes de qualquer commit do `repo_monitor`, é recomendável executar:

``` bash
git status
```

e confirmar que `.env` não aparece entre os arquivos que serão
versionados.

**Nunca publicar, compartilhar ou fazer commit do token.**

Para facilitar a configuração por outros integrantes no futuro, pode ser
criado um `.env.example` versionado:

``` env
GITHUB_TOKEN=seu_token_aqui
GITHUB_OWNER=nome_da_organizacao
GITHUB_REPO=nome_do_repositorio
```

Cada usuário poderá então criar seu `.env` local.

## 7. Primeiro monitor --- informações do repositório e main

Foi criado:

``` text
src/monitor.py
```

O primeiro teste consultou o endpoint do repositório através da GitHub
REST API.

A autenticação retornou:

``` text
STATUS: 200
```

Resultado obtido:

``` text
Repositório: Residencia-Time2/saude-publica-protocolos-clinicos
Privado: True
Branch principal: main
Issues abertas: 0
```

O HTTP `200` confirmou que:

-   o token estava válido;
-   o `.env` estava sendo carregado;
-   as permissões eram suficientes;
-   o programa conseguia acessar o repositório privado;
-   a comunicação com a GitHub API estava funcionando.

Esse foi o primeiro marco funcional do projeto.

## 8. Monitoramento dos commits da main

O `monitor.py` foi ampliado para consultar os commits recentes da
`main`.

Execução:

``` bash
uv run python src/monitor.py
```

Resultado observado em 15/09/2026:

``` text
=== REPOSITÓRIO ===
Nome: Residencia-Time2/saude-publica-protocolos-clinicos
Branch principal: main
Privado: True

=== ÚLTIMOS COMMITS ===
c2e7814 | SueliHora | 2026-09-14T21:56:55Z
  chore: adiciona dependencias base do projeto (openai, pydantic, dotenv, pytest)

26e2c45 | SueliHora | 2026-09-14T21:29:52Z
  chore:uvlock atualization

fbc7c1c | SueliHora | 2026-09-14T21:27:57Z
  chore: remove build-system do pyproject.toml e desativa package para corrigir erro do uv sync

5ba1f74 | Patricia Zan | 2026-09-14T20:41:57Z
  [SETUP] Setup of base folder structure

37f9840 | Patricia Zan | 2026-09-14T20:18:04Z
  [SETUP] Project structure setup

04d6923 | Patricia Zan | 2026-09-14T20:17:53Z
  [SETUP] Project structure setup

a320654 | Patricia Zan | 2026-09-14T20:03:11Z
  [SETUP] init
```

Esse teste mostrou que a API consegue recuperar SHA, autor, data e
mensagem dos commits.

Entretanto, a `main` sozinha não representa necessariamente toda a
atividade do grupo, pois o processo de desenvolvimento utilizará
branches por tarefa ou por pessoa.

## 9. Segundo monitor --- branches

Para separar responsabilidades foi criado:

``` text
src/monitor_branches.py
```

A função inicial desse programa é consultar dinamicamente todas as
branches existentes no repositório.

Execução:

``` bash
uv run python src/monitor_branches.py
```

Resultado inicial:

``` text
=== BRANCHES DO REPOSITÓRIO ===
Total: 1

Branch: main
Último commit: c2e7814
```

No momento do teste havia somente a branch `main`.

A vantagem dessa abordagem é que os nomes das branches não ficam
cadastrados manualmente no programa. Quando uma nova branch for criada
no GitHub, ela poderá aparecer automaticamente na próxima consulta.

Por exemplo, se futuramente forem criadas:

``` text
main
feature/rag
feature/backend
silvio/documentacao
```

o monitor poderá descobri-las diretamente através da API.

## 10. Por que monitorar branches

Como o grupo pretende trabalhar em branches separadas, um integrante
pode possuir vários commits que ainda não chegaram à `main`.

Exemplo:

``` text
A --- B --- C             main
           \
            D --- E       feature/rag
```

Nesse caso, `D` e `E` são trabalho realizado na branch, mas ainda não
aparecem na `main`.

Portanto, para acompanhar corretamente a evolução do projeto, o monitor
deverá considerar:

-   branches existentes;
-   commits de cada branch;
-   autor dos commits;
-   data da última atividade;
-   Pull Requests;
-   integração das branches com a `main`.

## 11. Comparação futura com a main

Uma evolução planejada para `monitor_branches.py` é comparar cada branch
de trabalho com a `main`.

Exemplo:

``` text
feature/rag
À frente da main: 2 commits
Atrás da main: 1 commit
```

**À frente da main** indica commits existentes na branch que ainda não
fazem parte da `main`.

**Atrás da main** indica commits que já chegaram à `main`, mas ainda não
foram incorporados à branch de trabalho.

Essa informação permitirá identificar branches com trabalho novo e
branches que podem estar desatualizadas.

Essa funcionalidade ainda não está implementada nesta primeira versão.

## 12. Estrutura atual

A estrutura lógica do projeto neste estágio é:

``` text
repo_monitor/
├── src/
│   ├── monitor.py
│   └── monitor_branches.py
├── .env                 # local, não versionado
├── .gitignore
├── .python-version
├── pyproject.toml
├── uv.lock
└── README.md
```

Responsabilidades:

``` text
monitor.py
    └── informações gerais do repositório
        └── commits recentes da main

monitor_branches.py
    └── descoberta das branches
        └── último SHA de cada branch
```

## 13. Arquitetura atual

``` text
repo_monitor
     |
     | HTTPS + token
     v
GitHub REST API
     |
     v
Residencia-Time2/
saude-publica-protocolos-clinicos
     |
     +-- main
     |
     +-- branches futuras
```

O `repo_monitor` é somente consumidor das informações fornecidas pela
API.

## 14. Próximas etapas

A evolução planejada inclui:

1.  Mostrar autor, data e mensagem do último commit de cada branch.
2.  Consultar commits por branch.
3.  Comparar cada branch com a `main`.
4.  Mostrar quantidade de commits à frente e atrás da `main`.
5.  Monitorar Pull Requests abertas.
6.  Identificar branch de origem, autor e destino de cada PR.
7.  Monitorar status de GitHub Actions.
8.  Consolidar atividade dos integrantes do grupo.
9.  Criar uma saída resumida de status do projeto.
10. Posteriormente avaliar uma interface de bot para realizar consultas.

Uma saída futura poderia ser:

``` text
=== STATUS DO PROJETO ===

Branch: feature/rag
Última atividade: 15/09/2026
Autor: Silvio
Commits à frente da main: 3
Commits atrás da main: 1
Pull Request: aberta

Branch: feature/backend
Última atividade: 15/09/2026
Autor: Sueli
Commits à frente da main: 5
Commits atrás da main: 0
Pull Request: ainda não criada
```

## 15. Estado do projeto ao final desta etapa

Ao final desta primeira etapa, o `repo_monitor` já consegue:

-   executar em Python 3.10 utilizando `uv`;
-   carregar configurações de forma segura através de `.env`;
-   autenticar em um repositório privado do GitHub;
-   consultar informações gerais do repositório;
-   identificar a branch principal;
-   recuperar commits recentes da `main`;
-   recuperar autor, data, mensagem e SHA dos commits;
-   descobrir dinamicamente as branches existentes;
-   identificar o último SHA de cada branch.

O próximo marco será transformar `monitor_branches.py` de um simples
descobridor de branches em um monitor de atividade por branch.

# Etapa 2 — Integração com Telegram

**Data:** 15/09/2026

## 16. Objetivo da segunda etapa

Após validar o acesso ao repositório privado através da GitHub REST API e os primeiros monitores executados pelo terminal, iniciou-se a segunda etapa do projeto: disponibilizar as consultas através de um bot no Telegram.

A proposta é permitir que os integrantes consultem o estado do projeto sem precisar executar diretamente os scripts Python.

A arquitetura passou a ser:

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
Residencia-Time2/
saude-publica-protocolos-clinicos
```

O bot possui função de consulta. Ele não realiza alterações no repositório monitorado.

## 17. Criação do bot no Telegram

Foi criado um bot exclusivo para o projeto através do BotFather.

Nome utilizado:

```text
RepoMonitor_bot
```

O BotFather forneceu um token de autenticação exclusivo.

Por segurança, o token não foi colocado diretamente no código-fonte.

Foi adicionada uma nova variável ao arquivo `.env`:

```env
TELEGRAM_TOKEN=seu_token_aqui
```

O arquivo `.env` continua protegido pelo `.gitignore` e não deve ser versionado.

Assim, o projeto passou a utilizar duas credenciais independentes:

```text
GITHUB_TOKEN
    |
    +-- acesso de leitura à GitHub REST API

TELEGRAM_TOKEN
    |
    +-- autenticação do RepoMonitor_bot
```

## 18. Instalação da biblioteca Telegram

A integração foi implementada utilizando a biblioteca:

```text
python-telegram-bot
```

Como o projeto utiliza `uv`, a dependência foi adicionada com:

```bash
uv add python-telegram-bot
```

O `uv` atualizou as dependências do projeto e seu arquivo de lock.

## 19. Primeiro teste do bot

Foi criado:

```text
src/bot_repo_monitor.py
```

Inicialmente o bot foi implementado sem acesso ao GitHub, com o objetivo de testar somente o fluxo:

```text
Telegram
    |
    v
bot_repo_monitor.py
    |
    v
Ubuntu
    |
    v
Resposta ao Telegram
```

Foram implementados inicialmente os comandos:

```text
/start
/status
```

O bot foi iniciado com:

```bash
uv run python src/bot_repo_monitor.py
```

O comando `/start` confirmou que o bot estava ativo.

O `/status`, nessa primeira versão, retornava apenas uma mensagem de teste.

Essa abordagem permitiu validar a comunicação com o Telegram antes de integrar a GitHub API.

## 20. Refatoração da comunicação com GitHub

Antes de conectar o Telegram ao monitoramento real, foi identificada a necessidade de separar a lógica de acesso à GitHub API da lógica de apresentação dos resultados.

Anteriormente, `monitor.py` realizava tanto a consulta quanto a apresentação no terminal.

Para evitar duplicação de código foi criado:

```text
src/github_api.py
```

A arquitetura passou a ser:

```text
                    github_api.py
                         |
          +--------------+--------------+
          |              |              |
          v              v              v
     monitor.py   monitor_branches.py   bot_repo_monitor.py
```

Dessa forma, terminal e Telegram podem utilizar as mesmas funções de acesso ao GitHub.

## 21. Funções centralizadas em github_api.py

O módulo `github_api.py` passou a carregar as configurações:

```text
GITHUB_TOKEN
GITHUB_OWNER
GITHUB_REPO
```

e centralizar a comunicação com a GitHub REST API.

As primeiras funções implementadas foram:

```python
consultar_repositorio()
consultar_commits()
consultar_branches()
```

A comunicação utiliza:

```text
requests
python-dotenv
```

O token é enviado no cabeçalho da requisição e nunca é exibido na saída do programa.

## 22. Validação da nova camada

Após a criação de `github_api.py`, foi realizado um teste independente:

```bash
uv run python -c "from src.github_api import consultar_repositorio; print(consultar_repositorio()['full_name'])"
```

O resultado esperado e obtido foi:

```text
Residencia-Time2/saude-publica-protocolos-clinicos
```

Isso confirmou que a nova camada de acesso à API estava funcionando antes de conectá-la ao Telegram.

## 23. Integração do /status com GitHub

Depois da validação de `github_api.py`, o comando `/status` do Telegram deixou de retornar uma mensagem estática e passou a realizar uma consulta real ao GitHub.

O fluxo passou a ser:

```text
/status
   |
   v
bot_repo_monitor.py
   |
   +-- consultar_repositorio()
   |
   +-- consultar_commits(limite=1)
   |
   v
GitHub REST API
   |
   v
Resposta ao Telegram
```

O `/status` passou a retornar informações como:

```text
STATUS DO REPOSITÓRIO

Repositório
Branch principal
Issues abertas

Último commit da main
Autor
Data
Mensagem
```

Nesse momento foi validado o fluxo completo:

```text
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
Repositório privado
   |
   v
Resposta ao usuário
```

## 24. Implementação do comando /branches

Após o funcionamento do `/status`, foi implementado o comando:

```text
/branches
```

O comando utiliza:

```python
consultar_branches()
```

e consulta dinamicamente as branches existentes.

A resposta inicial, enquanto o repositório possuía somente a `main`, era equivalente a:

```text
BRANCHES DO REPOSITÓRIO

Total: 1

main
Último commit: c2e7814
```

A lista não é cadastrada manualmente.

Quando novas branches forem criadas, elas poderão ser descobertas automaticamente pela próxima consulta à API.

## 25. Estado da arquitetura após a Etapa 2

Ao final desta etapa, a estrutura principal passou a ser:

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

As responsabilidades estão separadas da seguinte forma:

```text
github_api.py
    |
    +-- comunicação centralizada com GitHub

monitor.py
    |
    +-- monitoramento pelo terminal

monitor_branches.py
    |
    +-- monitoramento de branches pelo terminal

bot_repo_monitor.py
    |
    +-- interface de consulta através do Telegram
```

## 26. Comandos disponíveis no Telegram

A interface Telegram evoluiu a partir dos três comandos iniciais:

```text
/start
/status
/branches
```

O objetivo é transformar o bot em uma interface simples de consulta ao estado do repositório, sem exigir que cada integrante acesse o terminal do servidor.

### /start

O comando `/start` permanece público e tem duas funções:

1. confirmar que o bot está ativo;
2. informar o **Telegram ID** do usuário.

Exemplo:

```text
🤖 Repo Monitor

👤 Nome: Fulano da Silva
📱 Telegram: @fulano
🆔 Telegram ID: 123456789

Use /help para ver os comandos disponíveis.
```

Esse ID é utilizado no processo de liberação de acesso descrito na seção de controle de usuários.

### /status

Consulta informações gerais do repositório e o último commit disponível.

Exemplo:

```text
📊 STATUS DO REPOSITÓRIO

📁 Residencia-Time2/saude-publica-protocolos-clinicos
🌿 Branch principal: main

📝 Último commit
Autor: Nome do autor
Data: 2026-09-20T18:32:10Z
Mensagem: atualização do projeto
```

### /branches

Lista dinamicamente as branches existentes e o último SHA conhecido em cada uma.

Exemplo:

```text
🌿 BRANCHES DO REPOSITÓRIO

Total: 2

🌿 main
Último commit: a1b2c3d

🌿 feature/fetch-corpus
Último commit: e4f5g6h
```

A lista não é cadastrada manualmente. Quando uma nova branch for criada no GitHub, ela poderá aparecer automaticamente na próxima consulta.

### /help

Foi adicionado o comando `/help` para que os integrantes não precisem memorizar a interface do bot.

Exemplo:

```text
🤖 REPO MONITOR - COMANDOS DISPONÍVEIS

▶ /status
Mostra a situação geral do repositório.

▶ /branches
Lista as branches existentes.

▶ /commits
Mostra os últimos commits realizados.

▶ /activity
Mostra um panorama da atividade recente.

▶ /prs
Lista os Pull Requests abertos.

▶ /issues
Lista as issues abertas.

▶ /summary
Mostra um resumo geral do repositório.

▶ /help
Mostra esta lista de comandos.
```

### Comandos em expansão

Além dos comandos já validados, o bot está sendo ampliado para suportar:

```text
/commits
/activity
/prs
/issues
/summary
```

A finalidade de cada um é:

- `/commits`: listar os últimos commits, incluindo SHA, autor, data e mensagem;
- `/activity`: apresentar um panorama da atividade recente, evitando duplicar a função de `/commits`;
- `/prs`: listar Pull Requests abertas, mostrando autor, branch de origem e branch de destino;
- `/issues`: listar issues abertas e seus responsáveis quando houver;
- `/summary`: consolidar, em uma única resposta, branches, commits, PRs, issues e a última atividade.

Exemplo conceitual de `/summary`:

```text
📊 RESUMO DO REPOSITÓRIO

📁 Residencia-Time2/saude-publica-protocolos-clinicos
🌿 Branches: 2
📝 Commits recentes: 5
🔀 Pull Requests abertas: 1
📌 Issues abertas: 2

🕐 ÚLTIMA ATIVIDADE
👤 Nome do autor
📅 2026-09-20 17:40
💬 adiciona nova funcionalidade
```

A distinção entre `/commits` e `/activity` é importante:

```text
/commits
    -> histórico direto dos commits

/activity
    -> visão resumida da atividade recente do projeto
       incluindo commits, branches, PRs e issues
```


## 27. Decisão arquitetural

Uma decisão importante desta etapa foi não implementar chamadas diretas entre o bot e os programas de terminal.

Por exemplo, evitou-se:

```text
bot_repo_monitor.py
        |
        v
   monitor.py
```

Foi adotado:

```text
                 github_api.py
                 /     |     \
                /      |      \
               v       v       v
          monitor   branches   bot
```

Essa separação evita duplicação e facilita a evolução do projeto.

Quando uma nova consulta à GitHub API for necessária, ela poderá ser implementada uma única vez em `github_api.py` e reutilizada pelas diferentes interfaces.

## 28. Próximas evoluções

Após a integração inicial com o Telegram, parte das evoluções anteriormente previstas começou a ser incorporada ao projeto.

As funções de consulta ao GitHub passaram a incluir também:

```python
consultar_pulls()
consultar_issues()
```

Essas funções permanecem centralizadas em `github_api.py`, preservando a separação entre:

```text
github_api.py
    -> acesso à GitHub REST API

bot_repo_monitor.py
    -> comandos e respostas do Telegram
```

As próximas evoluções técnicas incluem:

- consultar commits por branch;
- comparar cada branch com a `main`;
- calcular commits à frente e atrás da `main`;
- enriquecer `/activity` com uma janela temporal, por exemplo últimas 24 horas ou últimos 7 dias;
- monitorar GitHub Actions;
- melhorar tratamento centralizado de erros;
- registrar logs operacionais do bot;
- validar todos os novos comandos com os integrantes do grupo.

Um exemplo futuro de comparação de branch:

```text
🌿 feature/rag

À frente da main: 3 commits
Atrás da main: 1 commit
Última atividade: 20/09/2026
Pull Request: aberta
```


## 29. Marco alcançado

Ao final da Etapa 2, o projeto deixou de ser apenas um conjunto de scripts locais de monitoramento.

Agora existe uma interface remota:

```text
Pessoa
   |
   v
Telegram
   |
   v
Repo Monitor
   |
   v
GitHub
```

Isso permite consultar o estado do repositório privado através do Telegram sem acessar diretamente o terminal do servidor.

O projeto mantém separadas:

- credenciais do GitHub;
- credenciais do Telegram;
- comunicação com a GitHub API;
- interface de terminal;
- interface Telegram.

Essa estrutura fornece uma base para a expansão do monitoramento nas próximas etapas.

# Etapa 3 — Controle de acesso, execução permanente e expansão do bot

**Data:** 20/09/2026

## 30. Controle de acesso por Telegram ID

Como o bot consulta um repositório privado, foi criado um mecanismo simples de autorização por Telegram ID.

O fluxo definido é:

```text
Usuário
   |
   | envia /start
   v
RepoMonitor_bot
   |
   | retorna Telegram ID
   v
Usuário envia o ID ao administrador
   |
   v
Administrador adiciona o ID ao .env
   |
   v
TELEGRAM_ALLOWED_USERS
   |
   v
Comandos protegidos são liberados
```

A variável utilizada é:

```env
TELEGRAM_ALLOWED_USERS=123456789,987654321
```

Os IDs são separados por vírgula.

No código, os usuários autorizados são carregados para um conjunto:

```python
ALLOWED_USERS = {
    int(user_id.strip())
    for user_id in os.getenv("TELEGRAM_ALLOWED_USERS", "").split(",")
    if user_id.strip()
}
```

A primeira validação é feita por:

```python
def usuario_autorizado(update: Update) -> bool:
    return update.effective_user.id in ALLOWED_USERS
```

Para evitar repetir o mesmo bloco em todos os comandos, foi criada uma função auxiliar:

```python
async def verificar_acesso(update: Update) -> bool:
    if usuario_autorizado(update):
        return True

    await update.message.reply_text(
        "⛔ Acesso não autorizado.\n\n"
        f"Seu Telegram ID: {update.effective_user.id}\n"
        "Solicite ao administrador a liberação do acesso."
    )

    return False
```

Assim, cada comando protegido pode iniciar com:

```python
if not await verificar_acesso(update):
    return
```

O `/start` permanece sem essa proteção porque ele precisa informar o Telegram ID ao usuário ainda não autorizado.

## 31. Separação entre autenticação do GitHub e autorização do Telegram

O projeto possui duas camadas distintas de segurança:

```text
GITHUB_TOKEN
    -> autoriza o servidor a consultar o repositório privado

TELEGRAM_ALLOWED_USERS
    -> define quais usuários podem solicitar consultas pelo bot
```

Essa separação é importante porque um usuário do Telegram não recebe acesso direto ao token do GitHub.

O fluxo real é:

```text
Usuário autorizado
      |
      v
Telegram
      |
      v
bot_repo_monitor.py
      |
      v
github_api.py
      |
      | GITHUB_TOKEN
      v
GitHub REST API
```

## 32. Execução permanente com systemd

O bot foi configurado para executar continuamente no notebook Ubuntu através de um serviço `systemd`.

O serviço utilizado é:

```text
repo-monitor.service
```

O processo é iniciado com o Python do ambiente virtual do projeto:

```text
/home/silvio/projetos/repo_monitor/.venv/bin/python
```

apontando para:

```text
/home/silvio/projetos/repo_monitor/src/bot_repo_monitor.py
```

A situação do serviço pode ser consultada com:

```bash
sudo systemctl status repo-monitor
```

Quando está funcionando corretamente, o estado esperado é:

```text
Active: active (running)
```

Após alterações no código ou no `.env`, o serviço deve ser reiniciado:

```bash
sudo systemctl restart repo-monitor
```

Para consultar erros recentes:

```bash
sudo journalctl -u repo-monitor -n 50 --no-pager
```

Esse comando foi importante durante a implementação porque permitiu localizar erros de execução, como funções ainda não definidas no `bot_repo_monitor.py`.

Exemplo de erro identificado:

```text
NameError: name 'help_command' is not defined
```

Outro erro identificado durante a evolução foi:

```text
NameError: name 'verificar_acesso' is not defined
```

Esses casos mostraram a utilidade do `journalctl` para depurar um serviço executado em segundo plano.

## 33. Ampliação de github_api.py

O módulo `github_api.py` foi ampliado para centralizar novas consultas.

Além de:

```python
consultar_repositorio()
consultar_commits()
consultar_branches()
```

foram adicionadas:

```python
consultar_pulls()
consultar_issues()
```

### Consulta de Pull Requests

A função consulta o endpoint de Pull Requests abertas e devolve os dados para o bot formatar.

Exemplo simplificado:

```python
def consultar_pulls():
    response = requests.get(
        f"{BASE_URL}/pulls",
        headers=HEADERS,
        params={"state": "open"},
        timeout=30,
    )

    response.raise_for_status()
    return response.json()
```

### Consulta de issues

A API do GitHub retorna Pull Requests também no endpoint de issues. Por isso foi necessário filtrar os itens que possuem o campo `pull_request`.

Exemplo:

```python
def consultar_issues():
    response = requests.get(
        f"{BASE_URL}/issues",
        headers=HEADERS,
        params={"state": "open"},
        timeout=30,
    )

    response.raise_for_status()

    dados = response.json()

    return [
        issue
        for issue in dados
        if "pull_request" not in issue
    ]
```

Essa filtragem evita contar uma Pull Request duas vezes: uma vez como PR e outra como issue.

## 34. Papel dos novos comandos

A expansão do bot foi planejada para responder perguntas diferentes sobre o estado do projeto.

### /commits

Foco: histórico recente de alterações.

Exemplo:

```text
📝 ÚLTIMOS COMMITS

🔹 a1b2c3d
👤 Nome do autor
📅 2026-09-20T17:30:00Z
💬 adiciona suporte ao novo comando
```

### /activity

Foco: panorama geral da atividade recente.

Exemplo:

```text
📈 ATIVIDADE RECENTE

📝 Commits recentes: 7
🌿 Branches: 2
🔀 Pull Requests abertas: 1
📌 Issues abertas: 3

🕐 ÚLTIMA ATIVIDADE
👤 Nome do autor
📅 2026-09-20 17:40
💬 atualiza documentação
```

Essa definição evita duplicidade entre `/activity` e `/commits`.

### /prs

Foco: Pull Requests que aguardam integração.

Exemplo:

```text
🔀 PULL REQUESTS ABERTOS

#12 - adiciona busca de protocolos
👤 usuario-github
🌿 feature/protocolos → main
```

### /issues

Foco: pendências registradas no GitHub.

Exemplo:

```text
📌 ISSUES ABERTAS

#8 - revisar estrutura do corpus
👤 Criada por: usuario-github
🎯 Responsável: outro-usuario
```

### /summary

Foco: visão condensada do estado atual.

Exemplo:

```text
📊 RESUMO DO REPOSITÓRIO

🌿 Branches: 2
📝 Commits recentes: 5
🔀 Pull Requests abertas: 1
📌 Issues abertas: 2
```

## 35. Tratamento de erros e validação

Antes de reiniciar o serviço após alterações no código, é recomendável validar a sintaxe Python:

```bash
python -m py_compile src/bot_repo_monitor.py
```

Se não houver saída, a sintaxe está válida.

Em seguida:

```bash
sudo systemctl restart repo-monitor
sudo systemctl status repo-monitor
```

Se o bot não responder a um comando, o próximo passo é consultar:

```bash
sudo journalctl -u repo-monitor -n 50 --no-pager
```

Essa sequência reduz o tempo de diagnóstico.

## 36. Estado atual consolidado

A arquitetura consolidada é:

```text
Integrante autorizado
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
        +-- valida Telegram ID
        |
        v
github_api.py
        |
        +-- consultar_repositorio()
        +-- consultar_commits()
        +-- consultar_branches()
        +-- consultar_pulls()
        +-- consultar_issues()
        |
        v
GitHub REST API
        |
        v
Residencia-Time2/
saude-publica-protocolos-clinicos
```

O bot permanece somente como ferramenta de consulta. Nenhuma função implementada nesta etapa altera arquivos, branches, issues ou Pull Requests no repositório.

O principal ganho desta evolução foi transformar o projeto em um monitor remoto com:

- acesso controlado por Telegram ID;
- execução contínua através de `systemd`;
- consultas centralizadas em `github_api.py`;
- interface de ajuda com `/help`;
- base pronta para os comandos `/commits`, `/activity`, `/prs`, `/issues` e `/summary`;
- diagnóstico operacional através de `systemctl` e `journalctl`.

