import logging
import telebot
import config
import datetime
import random
import os
from time import sleep
import threading

logging.basicConfig(level=logging.INFO)
bot = telebot.TeleBot(config.TOKEN)
user_ids = dict()


def set_up():
    with open("ids.txt") as f:
        for line in f.readlines():
            user_ids[int(line)] = set()


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    user_id = message.from_user.id
    if user_id not in user_ids:
        user_ids[user_id] = set()
        with open("ids.txt", 'a') as f:
            f.write(str(user_id) + '\n')
    bot.reply_to(message, "Отлично, теперь тебе будут приходить котики и ёжики")


def sendns():
    animals = ["cat", "hedgehog"]
    if 29 <= datetime.datetime.now().minute <= 31 or datetime.datetime.now().minute <= 1:
        for _id in user_ids:
            index = random.randint(0, len(animals) - 1)
            for file in os.listdir(os.path.join(os.getcwd(), f"{animals[index]}_pics")):
                if file in user_ids[_id] or os.path.getsize(os.path.join(f"{animals[index]}_pics", file)) < 50_000:
                    continue
                # data = 0
                # with open(os.path.join(f"{animals[index]}_pics", file), 'rb') as f:
                #     data = f.readline()
                f = open(os.path.join(f"{animals[index]}_pics", file), 'rb')
                try:
                    bot.send_photo(_id, f)
                    user_ids[_id].add(file)
                    break
                finally:
                    f.close()
        sleep(28 * 60)
    else:
        sleep(10)
    sendns()


def run():
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        sleep(10)
        run()


def start_bot():
    set_up()
    run()


def start_sending():
    try:
        sendns()
    except Exception as e:
        sleep(10)
        start_sending()


def main():
    t1 = threading.Thread(target=start_bot)
    t2 = threading.Thread(target=start_sending)
    t1.start()
    t2.start()


if __name__ == '__main__':
    main()
