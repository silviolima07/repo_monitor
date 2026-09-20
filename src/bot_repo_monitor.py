import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from github_api import (
    consultar_repositorio,
    consultar_commits,
    consultar_branches,
    consultar_pulls,
    consultar_issues,
)

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")

ALLOWED_USERS = {
   int(user_id.strip())
   for user_id in os.getenv("TELEGRAM_ALLOWED_USERS", "").split(",")
   if user_id.strip()
}

def usuario_autorizado(update: Update) -> bool:
    return update.effective_user.id in ALLOWED_USERS

async def verificar_acesso(update: Update) -> bool:
    if usuario_autorizado(update):
        return True

    await update.message.reply_text(
        "⛔ Acesso não autorizado.\n\n"
        f"Seu Telegram ID: {update.effective_user.id}\n"
        "Solicite ao administrador a liberação do acesso."
    )


if not TOKEN:
    raise RuntimeError("TELEGRAM_TOKEN não encontrado no .env")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    usuario = update.effective_user

    nome = usuario.full_name
    username = f"@{usuario.username}" if usuario.username else "não informado"
 
    telegram_id = usuario.id

    resposta = (
        "🤖 Repo Monitor\n\n"
        f"👤 Nome: {nome}\n"
        f"📱 Telegram: {username}\n"
        f"🆔 Telegram ID: {telegram_id}\n\n"
        "Use /status para consultar o repositório."
    )

    await update.message.reply_text(resposta)

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not usuario_autorizado(update):
        await update.message.reply_text(
            "⛔ Acesso não autorizado.\n\n"
            f"Seu Telegram ID: {update.effective_user.id}\n"
            "Solicite ao administrador a liberação do acesso."
        )
        return


    try:
        repo = consultar_repositorio()
        commits = consultar_commits(limite=1)

        ultimo = commits[0]
        autor = ultimo["commit"]["author"]["name"]
        mensagem = ultimo["commit"]["message"].split("\n")[0]
        data = ultimo["commit"]["author"]["date"]

        resposta = (
            "📊 STATUS DO REPOSITÓRIO\n\n"
            f"📁 {repo['full_name']}\n"
            f"🌿 Branch principal: {repo['default_branch']}\n"
            f"🐛 Issues abertas: {repo['open_issues_count']}\n\n"
            "📝 Último commit da main\n"
            f"Autor: {autor}\n"
            f"Data: {data}\n"
            f"Mensagem: {mensagem}"
        )

        await update.message.reply_text(resposta)

    except Exception as erro:
        await update.message.reply_text(
            f"❌ Erro ao consultar o GitHub: {erro}"
        )

async def branches(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not usuario_autorizado(update):
        await update.message.reply_text(
            "⛔ Acesso não autorizado.\n\n"
            f"Seu Telegram ID: {update.effective_user.id}\n"
            "Solicite ao administrador a liberação do acesso."
        )
        return


    try:
        lista = consultar_branches()

        resposta = f"🌿 BRANCHES DO REPOSITÓRIO\n\nTotal: {len(lista)}\n\n"

        for branch in lista:
            nome = branch["name"]
            sha = branch["commit"]["sha"][:7]

            resposta += (
                f"🌿 {nome}\n"
                f"Último commit: {sha}\n\n"
            )

        await update.message.reply_text(resposta)

    except Exception as erro:
        await update.message.reply_text(
            f"❌ Erro ao consultar branches: {erro}"
        )



async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not await verificar_acesso(update):
        return

    resposta = (
        "🤖 REPO MONITOR - COMANDOS DISPONÍVEIS\n\n"

        "▶ /status\n"
        "Mostra a situação geral do repositório.\n\n"

        "▶ /branches\n"
        "Lista as branches existentes.\n\n"

        "▶ /commits\n"
        "Mostra os últimos commits realizados.\n\n"

        "▶ /activity\n"
        "Mostra a atividade recente do projeto.\n\n"

        "▶ /prs\n"
        "Lista os Pull Requests abertos.\n\n"

        "▶ /issues\n"
        "Lista as issues abertas.\n\n"

        "▶ /summary\n"
        "Mostra um resumo geral do repositório.\n\n"

        "▶ /help\n"
        "Mostra esta lista de comandos."
    )

    await update.message.reply_text(resposta)


async def commits(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await verificar_acesso(update):
        return

    try:
        lista = consultar_commits(limite=10)

        resposta = "📝 ÚLTIMOS COMMITS\n\n"

        for item in lista:
            commit = item["commit"]

            resposta += (
                f"🔹 {item['sha'][:7]}\n"
                f"👤 {commit['author']['name']}\n"
                f"📅 {commit['author']['date']}\n"
                f"💬 {commit['message'].split(chr(10))[0]}\n\n"
            )

        await update.message.reply_text(resposta)

    except Exception as erro:
        await update.message.reply_text(
            f"❌ Erro ao consultar commits: {erro}"
        )


async def activity(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not await verificar_acesso(update):
        return

    try:
        commits = consultar_commits(limite=10)
        branches = consultar_branches()
        prs = consultar_pulls()
        issues = consultar_issues()

        resposta = (
            "📈 ATIVIDADE RECENTE\n\n"
            f"📝 Commits recentes: {len(commits)}\n"
            f"🌿 Branches: {len(branches)}\n"
            f"🔀 Pull Requests abertas: {len(prs)}\n"
            f"📌 Issues abertas: {len(issues)}\n"
        )

        if commits:
            ultimo = commits[0]["commit"]

            autor = ultimo["author"]["name"]
            mensagem = ultimo["message"].split("\n")[0]
            data = ultimo["author"]["date"].replace("T", " ")[:16]

            resposta += (
                "\n🕐 ÚLTIMA ATIVIDADE\n"
                f"👤 {autor}\n"
                f"📅 {data}\n"
                f"💬 {mensagem}"
            )

        await update.message.reply_text(resposta)

    except Exception as erro:
        await update.message.reply_text(
            f"❌ Erro ao consultar atividade: {erro}"
        )

async def prs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await verificar_acesso(update):
        return

    try:
        lista = consultar_pulls()

        if not lista:
            await update.message.reply_text(
                "🔀 Nenhum Pull Request aberto."
            )
            return

        resposta = "🔀 PULL REQUESTS ABERTOS\n\n"

        for pr in lista:
            resposta += (
                f"#{pr['number']} - {pr['title']}\n"
                f"👤 {pr['user']['login']}\n"
                f"🌿 {pr['head']['ref']} → {pr['base']['ref']}\n\n"
            )

        await update.message.reply_text(resposta)

    except Exception as erro:
        await update.message.reply_text(
            f"❌ Erro ao consultar Pull Requests: {erro}"
        )


async def issues(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await verificar_acesso(update):
        return

    try:
        lista = consultar_issues()

        if not lista:
            await update.message.reply_text(
                "📌 Nenhuma issue aberta."
            )
            return

        resposta = "📌 ISSUES ABERTAS\n\n"

        for issue in lista:
            resposta += (
                f"#{issue['number']} - {issue['title']}\n"
                f"👤 {issue['user']['login']}\n\n"
            )

        await update.message.reply_text(resposta)

    except Exception as erro:
        await update.message.reply_text(
            f"❌ Erro ao consultar issues: {erro}"
        )


async def summary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await verificar_acesso(update):
        return

    try:
        repo = consultar_repositorio()
        lista_branches = consultar_branches()
        lista_commits = consultar_commits(limite=5)
        lista_prs = consultar_pulls()
        lista_issues = consultar_issues()

        resposta = (
            "📊 RESUMO DO REPOSITÓRIO\n\n"
            f"📁 {repo['full_name']}\n"
            f"🌿 Branches: {len(lista_branches)}\n"
            f"📝 Commits recentes: {len(lista_commits)}\n"
            f"🔀 Pull Requests abertas: {len(lista_prs)}\n"
            f"📌 Issues abertas: {len(lista_issues)}\n"
        )

        if lista_commits:
            ultimo = lista_commits[0]["commit"]

            resposta += (
                "\n🕐 ÚLTIMA ATIVIDADE\n\n"
                f"👤 {ultimo['author']['name']}\n"
                f"📅 {ultimo['author']['date']}\n"
                f"💬 {ultimo['message'].split(chr(10))[0]}"
            )

        await update.message.reply_text(resposta)

    except Exception as erro:
        await update.message.reply_text(
            f"❌ Erro ao gerar resumo: {erro}"
        )

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("branches", branches))
    app.add_handler(CommandHandler("commits", commits))
    app.add_handler(CommandHandler("activity", activity))
    app.add_handler(CommandHandler("prs", prs))
    app.add_handler(CommandHandler("issues", issues))
    app.add_handler(CommandHandler("summary", summary))
    app.add_handler(CommandHandler("help", help_command))
     
    print("Repo Monitor Bot iniciado...")

    app.run_polling()


if __name__ == "__main__":
    main()



