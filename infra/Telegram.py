import json
import re

from functools import partial
from termcolor import colored
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

import consts
from game.Dialogo import Dialogo
from game.Game import Game
from game.User import User
from infra.Loader import Loader
from infra.Settings import Settings
from infra.State import State
from infra.Texts import Texts
from game.core import broadcast, controlar, enviar_mensaje, godspeak, keyboard_interaction, orden, register, respuesta_dialogo_textual, say, run, help, start, scan
from game.Arca import Arca

class Telegram:
    token: str
    def __init__(self, token: str, config: Settings, texts: Texts):
        print(colored(' 🤖 AURA assistant is initializing','green'))
        self.token = token
        game = Game()
        loader = Loader(config.save_endpoint, config.save_method)
        loader.load_into(game)

        app = Application.builder().token(token).build()
        state = State(config.bot_id, app.bot, loader, game, texts)

        app.add_handler(CommandHandler("start", partial(start_command, state)))
        app.add_handler(CommandHandler("ayuda".capitalize(), partial(help_command, state)))
        app.add_handler(MessageHandler(filters.TEXT, partial(handle_message, state)))
        app.add_handler(CallbackQueryHandler(partial(handle_button_callback, state)))
        app.add_error_handler(partial(handle_error, state))

        print(colored(' 🤖 AURA assistant is ready for duty','green'))
        app.run_polling(poll_interval=1)

async def start_command(state: State, update: Update, context: ContextTypes.DEFAULT_TYPE):
    code: str = update.message.text.replace("/start ", '')
    chat_id = context._chat_id
    if update.message.chat.type == 'group':
        chat_id = None
    user = state.game.user(context._user_id, chat_id)
    if code != '':
        code = re.sub("__?", clean_start_command, code)
        re_match = re.search("^[^ ]+", code.lower())
        command = re_match[0]
        rest = code[re_match.end(0)+1:]
        print(colored(f" 🔎 SCAN CODE command received: {command}, with value: {rest}","blue"))
        await handle_text_command(state, user, update, context, command, rest)
    else:
        await update.message.reply_text(start(state, user, code), parse_mode=ParseMode.HTML)

async def help_command(state: State, update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = context._chat_id
    if update.message.chat.type == 'group':
        chat_id = None

    user = state.game.user(context._user_id, chat_id)
    await update.message.reply_text(help(state, user), parse_mode=ParseMode.HTML)

async def handle_message(state: State, update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = context._chat_id
    message_type: str = update.message.chat.type
    text: str = update.message.text

    if message_type == 'group':
        chat_id = None
    user = state.game.user(context._user_id, chat_id)

    if user.dialogo != None:
        clean_text = text.strip()
        print(colored(f" ⚠️ - {user.describe()} has input dialog to modal {user.dialogo.tipo}/{user.dialogo.ruta}",'blue'))
        await update.message.reply_text(respuesta_dialogo_textual(state, user, user.dialogo, clean_text), parse_mode=ParseMode.HTML)
        return

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

async def handle_text_command(state: State, user: User, update: Update, context: ContextTypes.DEFAULT_TYPE, command: str, rest: str):
    match command:
        case 'register' | 'reg' | 'login':
            await update.message.reply_text(register(state, user, rest))
        case 'ayuda' | 'help' | 'h':
            await update.message.reply_text(help(state,user), parse_mode=ParseMode.HTML)
        case 'broadcast' | 'all' | 'broad' | 'todos' | 'emitir':
            await update.message.reply_text(await broadcast(state, user, rest), parse_mode=ParseMode.HTML)
        case 'msg' | 'mensaje' | 'susurro' | '':
            respuesta = await enviar_mensaje(state, user, rest)
            await update.message.reply_text(respuesta[0], reply_markup=respuesta[1], parse_mode=ParseMode.HTML)
        case 'godspeak':
            respuesta = await godspeak(state, user, rest)
            await update.message.reply_text(respuesta[0], reply_markup=respuesta[1], parse_mode=ParseMode.HTML)
        case 'haz' | 'ejecuta' | 'orden' | 'x':
            await update.message.reply_text(run(state,user,rest), parse_mode=ParseMode.HTML)
        case 'dime' | 'di' | 'imprime' | 'informa' | 'muestra' | 'i' | 'y':
            await update.message.reply_text(say(state,user,rest), parse_mode=ParseMode.HTML)
        case 'scan':
            respuesta = await scan(state,user,rest)
            await update.message.reply_text(respuesta[0], reply_markup=respuesta[1], parse_mode=ParseMode.HTML)
        case 'hola' | 'saludos' | 'saludo' | 'buenas' | 'w':
            await update.message.reply_text(state.txts.build_text(consts.TXT_SALUDO, {
                'nombre_tripulante': 'invitado' if user.avatar == None else user.avatar.name,
            }), parse_mode=ParseMode.HTML)
        case 'controlar':
            result = await controlar(state, user)
            await update.message.reply_text(result[0], reply_markup=result[1], parse_mode=ParseMode.HTML)
        case 'tarea' | 'atarear' | 'asignar':
            await update.message.reply_text(await orden(state, user, rest), parse_mode=ParseMode.HTML)
        case _:
            print(colored(f" ⚠️ - {user.describe()} has executed invalid command request: {command}",'yellow'))
            await update.message.reply_text(f"No existe el comando \"{command}\"")

async def handle_button_callback(state: State, update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query == None:
        return
    query = update.callback_query
    await query.answer()

    chat_id = context._chat_id
    user = state.game.user(context._user_id, chat_id)
    print(colored(f" ⚠️ - {user.describe()} pressed button for {query.data}",'green'))

    dia = Dialogo.from_tuple(json.loads(query.data))

    response = await keyboard_interaction(state, user, dia)

    await query.edit_message_text(text=response[0], reply_markup=response[1], parse_mode=ParseMode.HTML)

async def handle_error(state: State, update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(
        colored(' ❌ ERROR caused by context: ','red'), context.error,
        colored(update,'grey')
    )

def clean_start_command(match: re.Match[str]):
    if match.end(0) - match.start(0) > 1 :
        return "_"
    return " "
