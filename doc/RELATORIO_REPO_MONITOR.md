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
