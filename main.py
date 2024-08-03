import re

from os import read
from typing import Final
from functools import partial
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from logic import Bot_state, User_state, say, run, help
from texts import BOT_USERNAME, WELCOME, SALUDO

async def start_command(state: Bot_state, update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME)

async def help_command(state: Bot_state, update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = state.user(context._chat_id)
    await update.message.reply_text(help(state, user))

async def handle_message(state: Bot_state, update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    user = state.user(context._chat_id)

    command = ''
    rest = ''

    if message_type == 'group':
        if BOT_USERNAME not in text:
            return
        clean_text = text.replace(BOT_USERNAME, '', 1).strip()
        re_match = re.search("^[^ ]+", clean_text.lower())
        command = re_match[0]
        rest = clean_text[re_match.end(0)+1:]
    else:
        clean_text = text.strip()
        re_match = re.search("^[^ ]+", clean_text.lower())
        command = re_match[0]
        rest = clean_text[re_match.end(0)+1:]

    match command:
        case "ayuda":
            await update.message.reply_text(help())
        case "haz" | "ejecuta":
            await update.message.reply_text(run(state,user,rest))
        case "dime" | "imprime" | "informa" | "muestra":
            await update.message.reply_text(say(state,user,rest))
        case "hola" | "saludos" | "saludo":
            await update.message.reply_text(SALUDO)
        case _:
            print(f"Invalid command request: {command}")
            await update.message.reply_text(f"No existe el comando \"{command}\"")

async def handle_error(state: Bot_state, update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused and error: {context.error}")

if __name__ == '__main__':

    print(" 🤖 AURA assistant is initializing")

    # Token management
    token_file = open("token.secret", mode="r", encoding="utf-8")
    TOKEN: Final = token_file.read()
    token_file.close()

    state = Bot_state()

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", partial(start_command, state)))
    app.add_handler(CommandHandler("ayuda".capitalize(), partial(help_command, state)))
    app.add_handler(MessageHandler(filters.TEXT, partial(handle_message, state)))
    app.add_error_handler(partial(handle_error, state))

    print(" 🤖 AURA assistant is ready for duty")
    app.run_polling(poll_interval=1)
