import re

from functools import partial
from termcolor import colored
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from game.User import User
from infra.Loader import Loader
from infra.Settings import Settings
from infra.Texts import Texts
from game.core import Bot, say, run, help, start, scan
from game.Arca import Arca

class Telegram:
    token: str
    def __init__(self, token: str, config: Settings, texts: Texts):
        print(colored(' 🤖 AURA assistant is initializing','green'))
        self.token = token
        arca = Arca()
        state = Bot(config.bot_id, arca, texts)
        loader = Loader(config.save_endpoint, config.save_method)

        loader.load_into(state)

        app = Application.builder().token(token).build()

        app.add_handler(CommandHandler("start", partial(start_command, state)))
        app.add_handler(CommandHandler("ayuda".capitalize(), partial(help_command, state)))
        app.add_handler(MessageHandler(filters.TEXT, partial(handle_message, state)))
        app.add_error_handler(partial(handle_error, state))

        print(colored(' 🤖 AURA assistant is ready for duty','green'))
        app.run_polling(poll_interval=1)

async def start_command(state: Bot, update: Update, context: ContextTypes.DEFAULT_TYPE):
    code: str = update.message.text.replace("/start ", "")
    user = state.user(context._user_id)
    if code != "":
        code = re.sub("__?", clean_start_command, code)
        re_match = re.search("^[^ ]+", code.lower())
        command = re_match[0]
        rest = code[re_match.end(0)+1:]
        print(colored(f" 🔎 SCAN CODE command received: {command}, with value: {rest}","blue"))
        await handle_text_command(state, user, update, context, command, rest)
    else:
        await update.message.reply_text(start(state, user, code), parse_mode=ParseMode.MARKDOWN_V2)

async def help_command(state: Bot, update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = state.user(context._user_id)
    await update.message.reply_text(help(state, user), parse_mode=ParseMode.MARKDOWN_V2)

async def handle_message(state: Bot, update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    user = state.user(context._user_id)

    command = ''
    rest = ''

    if message_type == 'group':
        if state.id not in text:
            return
        clean_text = text.replace(state.id, '', 1).strip()
        re_match = re.search("^[^ ]+", clean_text.lower())
        command = re_match[0]
        rest = clean_text[re_match.end(0)+1:]
    else:
        clean_text = text.strip()
        re_match = re.search("^[^ ]+", clean_text.lower())
        command = re_match[0]
        rest = clean_text[re_match.end(0)+1:]

    await handle_text_command(state, user, update, context, command, rest)

async def handle_text_command(state: Bot, user: User, update: Update, context: ContextTypes.DEFAULT_TYPE, command: str, rest: str):
    match command:
        case "ayuda" | "help":
            await update.message.reply_text(help(state,user), parse_mode=ParseMode.MARKDOWN_V2)
        case "haz" | "ejecuta" | "orden":
            await update.message.reply_text(run(state,user,rest), parse_mode=ParseMode.MARKDOWN_V2)
        case "dime" | "imprime" | "informa" | "muestra":
            await update.message.reply_text(say(state,user,rest), parse_mode=ParseMode.MARKDOWN_V2)
        case "scan":
            await update.message.reply_text(scan(state,user,rest), parse_mode=ParseMode.MARKDOWN_V2)
        case "hola" | "saludos" | "saludo":
            await update.message.reply_text(state.txts.txt_saludo, parse_mode=ParseMode.MARKDOWN_V2)
        case _:
            print(colored(f" ⚠️ - Invalid command request: {command}",'yellow'))
            await update.message.reply_text(f"No existe el comando \"{command}\"")

async def handle_error(state: Bot, update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(
        colored(' ❌ ERROR caused by context: ','red'), context.error,
        colored(update,'grey')
    )

def clean_start_command(match: re.Match[str]):
    if match.end(0) - match.start(0) > 1 :
        return "_"
    return " "
