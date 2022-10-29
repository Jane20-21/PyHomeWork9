from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, Filters
from random import randint
import csv

bot_token = '5473119887:AAHt1kljasR5NBldSoXKFORuP7HlhiVMfek'
bot = Bot(bot_token)
updater = Updater(bot_token, use_context=True)
dispatcher = updater.dispatcher

# pip install python-telegram-bot==13.14
# Updater → Dispatсher → Handlers → start → wait_for_the_end
# Updater - взаимодействие между клиентом и сервером
# Dispatсher - отвечает за вызов обработчика сообщений
# Handlers - обработчики сообщений


def start(update, context):
    context.bot.send_message(update.effective_chat.id, f"Привет! Это телефонный справочник!\n Выберите просмотр /show \n Показать контакт под номером /number \n Удалить запись под номером /delete \n Добавить запись /add \n")

def show(update, context):
    context.bot.send_message(update.effective_chat.id, 'Введите название для справочника, после просмотра справочника, для выхода напишите /stop ')
    return 1

def show_output(update, context):
    update.message.reply_text(f'{update.message.text} \n {show_phone()}')

def show_phone():
    with open('d:\Geek\Введение в Python\PyHomeWork9\phone.csv', encoding='utf-8', newline='') as file:
        file_csv = csv.reader(file, delimiter=";")
        res = list(file_csv)
    return res

def number(update, context):
    context.bot.send_message(update.effective_chat.id, 'Введите номер записи, которую хотите увидеть:\n После просмотра записи, для выхода напишите /stop ')
    return 1

def number_output(update, context):
    update.message.reply_text(f'Запись с выбранным номером: {number_phone(update.message.text)}')

def number_phone(index):
    list_csv = show_phone()
    ind = int(index)
    res = list_csv[ind]
    return res

def delete(update, context):
    context.bot.send_message(update.effective_chat.id, 'Введите номер записи для удаления:\n После просмотра справочника, для выхода напишите /stop ')
    return 1

def delete_output(update, context):
    update.message.reply_text(f'Справочник с удаленной записью: \n {del_info(update.message.text)}')

def del_info(index):
    list_csv = show_phone()
    ind = int(index)
    del list_csv[ind]
    with open('d:\Geek\Введение в Python\PyHomeWork9\phone.csv', 'w', encoding="utf8", newline='') as file:
        writer = csv.writer(file, delimiter=';')
        for row in list_csv:
            writer.writerow(row)
    res = show_phone()
    return res

def add(update, context):
    context.bot.send_message(update.effective_chat.id, 'Введите новый контакт в формате Фамилия Имя Телефон Коментарий через пробел:\n После просмотра справочника, для выхода напишите /stop ')
    return 1

def add_output(update, context):
    update.message.reply_text(f'Справочник с добавленной записью: \n {add_info(update.message.text)}')

def add_info(list):
    in_info = list.split()
    with open('d:\Geek\Введение в Python\PyHomeWork9\phone.csv', 'a', encoding="utf8", newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(in_info)
    res = show_phone()
    return res

def stop(update, context):
    update.message.reply_text("Всего доброго!")
    return ConversationHandler.END


show_handler = ConversationHandler(
        entry_points=[CommandHandler('show', show)],

        # Состояние внутри диалога.
        states={
            1: [MessageHandler(Filters.text & ~Filters.command, show_output)],
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]
    )

number_handler = ConversationHandler(
        entry_points=[CommandHandler('number', number)],

        # Состояние внутри диалога.
        states={
            1: [MessageHandler(Filters.text & ~Filters.command, number_output)],
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]
    )

delete_handler = ConversationHandler(
        entry_points=[CommandHandler('delete', delete)],

        # Состояние внутри диалога.
        states={
            1: [MessageHandler(Filters.text & ~Filters.command, delete_output)],
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]
    )

add_handler = ConversationHandler(
        entry_points=[CommandHandler('add', add)],

        # Состояние внутри диалога.
        states={
            1: [MessageHandler(Filters.text & ~Filters.command, add_output)],
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]
    )

start_handler = CommandHandler('start', start)

dispatcher.add_handler(show_handler)
dispatcher.add_handler(number_handler)
dispatcher.add_handler(delete_handler)
dispatcher.add_handler(add_handler)
dispatcher.add_handler(start_handler)
updater.start_polling()
updater.idle()