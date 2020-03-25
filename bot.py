import requests
import json
import telebot
from _token import token

url = "https://covid-19-coronavirus-statistics.p.rapidapi.com/v1/stats"
querystring = {"country": ""}
headers = {
    'x-rapidapi-host': "covid-19-coronavirus-statistics.p.rapidapi.com",
    'x-rapidapi-key': "87c228d61bmsh9d6557cc14b79e5p156549jsn8a1e39e3dffa"
}

response = requests.request("GET", url, headers=headers, params=querystring)
json_data = json.loads(response.text)
data = json_data['data']['covid19Stats']
last_update = json_data['data']['covid19Stats'][0]['lastUpdate']
stats = {}

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


bot = telebot.TeleBot(token)
message_start_help = "Привет, {}! Тут ты можешь узнать полную статистику о COVID-19. " \
                     "Напиши 'хочу знать' и я выдам тебе статистику."

message_stat = f'Окей, вот статистика по всему миру(данные могуть быть с задержкой в несколько часов):\n' \
               f'Дата обновления статистики: {last_update}\n' \
               f'Подтверждённых случаев: {confirmed}\n' \
               f'Выздоровевших: {recovered}\n' \
               f'Смертей: {deaths}\n\n' \
               f'Карта с официальной статистикой:' \
               f'https://www.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6'

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    name_user = message.json['from']['first_name']
    bot.reply_to(message, message_start_help.format(name_user))


@bot.message_handler(content_types=['text'])
def reply_to_user(message):
    if message.text.lower() == 'хочу знать':
        bot.reply_to(message, message_stat)

    elif message.text.lower() == 'помощь':
        bot.send_message(message.chat.id, 'Ты можешь узнать полную статистику о COVID-19. '
                                          'Напиши "хочу знать" и я выдам тебе статистику.')

    elif message.text.lower() == 'привет' or message.text.lower() == 'привет!':
        name_user = message.json['from']['first_name']
        bot.reply_to(message, message_start_help.format(name_user))

    else:
        bot.reply_to(message, 'Не понимаю, напиши "хочу знать" либо "помощь"')


if __name__ == '__main__':
    bot.polling()
