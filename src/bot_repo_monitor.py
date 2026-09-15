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

ALLOWED_USERS = {
   int(user_id.strip())
   for user_id in os.getenv("TELEGRAM_ALLOWED_USERS", "").split(",")
   if user_id.strip()
}

def usuario_autorizado(update: Update) -> bool:
    return update.effective_user.id in ALLOWED_USERS

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

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("branches", branches))
    
    print("Repo Monitor Bot iniciado...")

    app.run_polling()


if __name__ == "__main__":
    main()
