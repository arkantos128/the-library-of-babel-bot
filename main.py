from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ParseMode
import logging
from config import *
from utils import *


def right_endings(word_param):
    if word_param == 'w':
        num = library['wall']
        words = ['стена', 'стены', 'стен']
    elif word_param == 's':
        num = library['shelf']
        words = ['полка', 'полки', 'полок']
    elif word_param == 'v':
        num = library['volume']
        words = ['том', 'тома', 'томов']
    elif word_param == 'p':
        num = library['page']
        words = ['страница', 'страницы', 'страниц']
    else:
        num = library['page_len']
        words = ['символ', 'символа', 'символов']
    ind = ending_class(num)
    return '{0} {1}'.format(num, words[ind])


def start(update, context):
    global current_state
    send_message = lambda message: context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    if current_state[0] == START:
        send_message('Для поиска по тексту отправь сообщение, состоящий из латинских букв в нижнем регистре, '
                     'пробела и точки длиной не более ' + str(library['page_len']) + ' символов.')
        send_message('Для поиска по адресу страницы отправь сообщение в формате '
                     '{адрес комнаты}-{стена}-{полка}-{том}-{страница}')
        send_message('В случае неправильного формата сообщение будет отчищено от лишних '
                     'симоволов и переведено в нижний регистр.')
        current_state[0] = WAITING_TEXT


def help(update, context):
    text = 'Поиска по тексту: латинские буквы в нижнем регистре, ' \
           'пробела и точки, длина сообщения не более ' + str(library['page_len']) + ' символов.\n'
    text += 'Поиска по адресу страницы: {адрес комнаты}-{стена}-{полка}-{том}-{страница}'
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def params(update, context):
    text = 'Текущие параметры Библиотеки:\n{0} в комнате\n{1} на стене\n{2} на полке\n' \
           '{3} в томе\n{4} на странице'.format(
        right_endings('w'),
        right_endings('s'),
        right_endings('v'),
        right_endings('p'),
        right_endings('pl'))
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def get_text(update, context):
    global current_state
    send_message = lambda message: context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    if current_state[0] == WAITING_TEXT:
        send_message('Ищем в чертогах библиотеки...')
        text = update.message.text.lower()
        if '-' in text:
            address = text
            if not check_address(address):
                send_message('Неверный формат адреса.')
                return
        else:
            text = clear_text(text)
            address = search_page(text)
            send_message('Адрес:\n' + address)

        title = get_title(address)
        send_message('Название книги:\n' + title)

        message = 'Текст:\n'
        message += get_page(address)
        message = message.replace(text, '<b>' + text + '</b>')
        context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode=ParseMode.HTML)

def main():
    updater = Updater(token=token)
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    handlers = [CommandHandler('start', start),
                CommandHandler('params', params),
                CommandHandler('help', help),
                MessageHandler(Filters.text & (~Filters.command), get_text)]

    for handler in handlers:
        dispatcher.add_handler(handler)

    updater.start_webhook(listen="0.0.0.0",
                          port=port,
                          url_path=token)
    updater.bot.set_webhook('https://{0}.herokuapp.com/{1}'.format(app_name, token))
    updater.idle()

if __name__ == '__main__':
    current_state = [START]
    main()
