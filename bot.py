import time
import os
import telebot
import pandas
import feedparser
import random
import schedule

from flask import Flask, request
from datetime import datetime
from time import mktime
from multiprocessing import *
from telebot import types


TOKEN = os.environ['BOT_API_TOKEN']
bot = telebot.TeleBot(TOKEN)
APP_URL = f'https://anti-technopolis-bot.herokuapp.com/{TOKEN}'
group_id = os.environ['GROUP_ID']
server = Flask(__name__)


def start_process():
    p1 = Process(target=TimeSchedule.start_schedule, args=()).start()


class TimeSchedule():
    def start_schedule():
        schedule.every().day.at("4:30").do(TimeSchedule.send_congratulations)

        while True:
            schedule.run_pending()
            time.sleep(1)


    def send_congratulations():
        data = pandas.read_csv("birthdays.csv")
        today = datetime.now()
        today_tuple = (today.month, today.day)
        birthdays_dict = {(data_row["month"], data_row["day"]): data_row for (index, data_row) in data.iterrows()}

        if today_tuple in birthdays_dict:
            birthday_person = birthdays_dict[today_tuple]
            name = birthday_person["name"]
            bot.send_message(group_id, f"С Днём Рождения {name}! 🎈🎈🎈🎂🎂🎂🍾🍾🍾")
        else:
            print('Сегодня нет именинников.')


@bot.message_handler(regexp='Денис когда Витя выложит эфир?')
def reply_new_podcast(message):
    podcast_url = feedparser.parse("https://promodj.com/strogonov-radioshow-technopolis/podcast.xml")
    podcast_link = podcast_url.entries[0]['link']
    post_date = datetime.fromtimestamp(mktime(podcast_url.entries[0].published_parsed)).date()
    today_date = datetime.now().date()

    if today_date == post_date:
        bot.send_message(message.chat.id, f'Вот держи свежий эфир радио-шоу "ТЕХНОПОЛИС" \n \n {podcast_link}')
    else:
        bot.send_message(message.chat.id, 'Витя ещё не выложил 😞😞😞')


@bot.message_handler(content_types=["pinned_message", "photo", "voice", "audio", "video"])
def reply_genius(message):
    random_answer = [
                    'совсем дерадировали...',
                    'сука подстава...',
                    'вы че блять угорать решили',
                    'нету развити, вы загнетесь как черви',
                    'юморист хренов',
                    'чтоб у вас мозги от хардкора повылетали',
                    'леха косит под витю',
                    'Ленар в Питере???',
                    'леха бухой алкаш',
                    'Леха алкоголик...',
                    'Ленар плохой он предатель перестал со мной общаться он кинул меня',
                    'Артем меня Чекатилой обзывает????',
                    'Пацаны я нормальный стал! пошли пиво пить???? я угощаю',
                    '((((((((((',
                    'Ты понял сам какую херню ты отправил сам...',
                    'ты вообще вминяемый или нет? или гомосек',
                    'а??',
                    'Хуйня',
                    'хуйня',
                    '👎👎👊👊👊',
                    'и че блять...',
                    '👎👎👎👎😡😡😡😡😡👎👎',
                    'Вы загнётесь как черви',
                    'У тебя есть свободные подруги ? Дай Контакты',
                    'какого хрена такое отправляешь ты адекватный вообще нормальный?',
    ]
    bot.send_message(message.chat.id, random.choice(random_answer), reply_to_message_id=message.message_id)


@server.route('/' + TOKEN, methods=['POST'])
def get_message():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '!', 200


@server.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL)
    return '!', 200


if __name__ == '__main__':
    start_process()
    server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))