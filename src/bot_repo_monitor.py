import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from github_api import (
    consultar_repositorio,
    consultar_commits,
    consultar_branches,
)

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TOKEN:
    raise RuntimeError("TELEGRAM_TOKEN não encontrado no .env")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Repo Monitor ativo!\n\n"
        "Use /status para consultar o repositório."
    )


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("branches", branches))
    
    print("Repo Monitor Bot iniciado...")

    app.run_polling()


if __name__ == "__main__":
    main()
