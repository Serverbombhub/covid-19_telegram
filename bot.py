import requests
import json
import logging
import telebot
from telebot import types
from _token import token

url = "https://covid-19-coronavirus-statistics.p.rapidapi.com/v1/stats"
querystring = {"country": ""}
headers = {
    'x-rapidapi-host': "covid-19-coronavirus-statistics.p.rapidapi.com",
    'x-rapidapi-key': "87c228d61bmsh9d6557cc14b79e5p156549jsn8a1e39e3dffa"
}

bot = telebot.TeleBot(token)
message_start_help = "Привет, {}! Тут ты можешь узнать полную статистику о COVID-19. " \
                     "Нажми 'хочу знать' и я выдам тебе статистику. " \
                     "Либо можно просто получить официальную карту."
get_stat_user = types.KeyboardButton('хочу знать')
help_user = types.KeyboardButton('помощь')
map_covid = types.KeyboardButton('хочу карту')


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(selective=True)
    name_user = message.json['from']['first_name']
    markup.row(get_stat_user, help_user)
    markup.row(map_covid)
    bot.send_message(message.chat.id, message_start_help.format(name_user), reply_markup=markup)


@bot.message_handler(func=lambda message: message.text.lower() == 'хочу знать')
def get_stats_user(message):
    response = requests.request("GET", url, headers=headers)
    json_data = json.loads(response.text)
    data = json_data['data']['covid19Stats']
    stats = {}
    last_check = json_data['data']['lastChecked']
    last_check = last_check[0:10] + ' ' + last_check[11:19]
    for x in data:
        if 'confirmed' in stats:
            stats['confirmed'] += x['confirmed']
        else:
            stats['confirmed'] = x['confirmed']
        if 'deaths' in stats:
            stats['deaths'] += x['deaths']
        else:
            stats['deaths'] = x['deaths']
        if 'recovered' in stats:
            stats['recovered'] += x['recovered']
        else:
            stats['recovered'] = x['recovered']

    confirmed, deaths, recovered = stats.values()

    message_stat = f'Окей, вот статистика по всему миру(данные могут быть с задержкой в несколько часов):\n' \
                   f'Дата обновления статистики: <b>{last_check}</b>\n' \
                   f'Подтверждённых случаев: <b>{confirmed}</b>\n' \
                   f'Выздоровевших: <b>{recovered}</b>\n' \
                   f'Смертей: <b>{deaths}</b>\n\n' \
                   f'Карта с официальной статистикой: ' \
                   f'https://www.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6'

    bot.reply_to(message, message_stat, parse_mode='html')


@bot.message_handler(func=lambda message: message.text.lower() == 'помощь')
def help_user_reply(message):
    markup = types.ReplyKeyboardMarkup(selective=True)
    fuck_bot = types.KeyboardButton('просто отвали')
    markup.row(get_stat_user, map_covid)
    markup.row(fuck_bot)
    bot.send_message(message.chat.id, "Ты можешь узнать полную статистику о COVID-19."
                                      "Нажми 'хочу знать' и  выдам тебе статистику."
                                      "Либо можно просто получить ссылку на официальную карту.", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text.lower() in ['привет', 'привет!', 'hi', 'hello'])
def welcome_user_reply(message):
    markup = types.ReplyKeyboardMarkup(selective=True)
    markup.row(get_stat_user, help_user)
    name_user = message.json['from']['first_name']
    bot.send_message(message.chat.id, message_start_help.format(name_user), reply_markup=markup)


@bot.message_handler(func=lambda message: message.text.lower() in ['просто отвали', 'пошел ты', 'пошёл ты', 'отвали'])
def fuck_user_reply(message):
    bot.reply_to(message, 'Ну и ладно, мне как-то всё равно.')


@bot.message_handler(func=lambda message: message.text.lower() == 'хочу карту')
def map_user_reply(message):
    bot.send_message(message.chat.id, 'Держи: '
                                      'https://www.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6')


@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(message):
    markup = types.ReplyKeyboardMarkup(selective=True)
    markup.row(get_stat_user, help_user)
    bot.send_message(message.chat.id, 'Не понимаю, нажми "хочу знать" либо "помощь"', reply_markup=markup)


if __name__ == '__main__':
    bot.polling(none_stop=True)
