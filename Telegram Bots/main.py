import telebot
from telebot import types

bot = telebot.TeleBot('5582859993:AAHnFoVfl_FTL_h8M9_YMd8KDPO1lNevhkw')

@bot.message_handler(commands=['start'])
def start(message):
    mess = f'Здравствуйте {message.from_user.username}, добро пожаловать в telegram bot, сделанный специально для нашего Hackathon проекта. Об основной информации о проекте и возможностях бота можно узнать по комманде /help.'
    bot.send_message(message.chat.id, mess)

@bot.message_handler(commands=['help'])
def start(message):
    mess = f'HackathonBot представляет возможности проекта в backend части.\nКомманды:\n- /start запустить бота\n- /help вывести информацию о возможностях бота\n Запросы:\n- social registration открывает ссылку на регестрацию через соц. сеть (только GitHub)\n- swagger открывает ссылку на swagger клиент\n- admin открывает ссылку на админ понель проекта\n'
    bot.send_message(message.chat.id, mess)

@bot.message_handler()
def get_user_text(message):
    if message.text == 'social registration':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Social registration --->', url='http://127.0.0.1:8000/'))
        bot.send_message(message.chat.id, 'Нажмите для перехода на регистрации через соц. сеть',reply_markup=markup)
    elif message.text == 'swagger':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Swagger --->', url='http://127.0.0.1:8000/docs/'))
        bot.send_message(message.chat.id, 'Нажмите для перехода на swagger клиент',reply_markup=markup)
    elif message.text == 'admin':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Django Administration --->', url='http://127.0.0.1:8000/admin/'))
        bot.send_message(message.chat.id, 'Нажмите для перехода на админ панель',reply_markup=markup)

    else:
        bot.send_message(message.chat.id, 'На такой запрос нет ответ, введите запрос заного.')

bot.polling(none_stop=True)