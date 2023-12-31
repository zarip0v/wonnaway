import telebot
import dateutil.parser
import os
import math
from dotenv import load_dotenv
from telebot import types
from api import api
from data import data

load_dotenv()
bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))

AIRPORTS = data.upload_airports()
CITIES = data.upload_cities()
COUNTRIES = data.upload_countries()


def menu(message):
    keyboard = types.ReplyKeyboardMarkup(True, False)
    btn1 = types.KeyboardButton('А куда чаще смотрят билеты?')
    btn2 = types.KeyboardButton('А куда чаще летают?')
    btn3 = types.KeyboardButton('Знаю когда, но куда?')
    btn4 = types.KeyboardButton('Знаю куда, но когда?')
    btn5 = types.KeyboardButton('А что по курсу валют?')
    keyboard.add(btn1)
    keyboard.add(btn2)
    keyboard.add(btn3)
    keyboard.add(btn4)
    keyboard.add(btn5)

    bot.send_message(message.from_user.id, "Давай куда-нибудь уедем!", reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/start":
        menu(message)
    elif message.text == "А куда чаще смотрят билеты?":
        keyboard = types.ReplyKeyboardMarkup(True, True)
        keyboard.add(types.KeyboardButton('Отправить местоположение', request_location=True))
        keyboard.add(types.KeyboardButton('Назад'))
        bot.send_message(message.from_user.id,
                         "Сейчас глянем. Кинь местоположение или введи трехбуквенный код или название "
                         "аэропорта/города (например, SVO или Москва):",
                         reply_markup=keyboard)
        bot.register_next_step_handler(message, get_often)
    elif message.text == "А куда чаще летают?":
        keyboard = types.ReplyKeyboardMarkup(True, False)
        btn1 = types.KeyboardButton('Аэрофлот')
        btn2 = types.KeyboardButton('S7 Airlines')
        btn3 = types.KeyboardButton('Utair')
        btn4 = types.KeyboardButton('Победа')
        btn5 = types.KeyboardButton('Назад')
        keyboard.add(btn1, btn2)
        keyboard.add(btn3, btn4)
        keyboard.add(btn5)
        bot.send_message(message.from_user.id,
                         "Сейчас глянем. Выбери авиакомпанию или введи ее двузначный код (например, SU для Аэрофлота):",
                         reply_markup=keyboard)
        bot.register_next_step_handler(message, get_companies)
    elif message.text == "Знаю куда, но когда?":
        keyboard = types.ReplyKeyboardMarkup(True, True)
        keyboard.add(types.KeyboardButton('Назад'))
        bot.send_message(message.from_user.id,
                         "Сейчас глянем. Отправь трехбуквенный код или название города отправления (например, "
                         "MOW или Москва):",
                         reply_markup=keyboard)
        bot.register_next_step_handler(message, get_when_1)
    elif message.text == "Знаю когда, но куда?":
        keyboard = types.ReplyKeyboardMarkup(True, True)
        keyboard.add(types.KeyboardButton('Назад'))
        bot.send_message(message.from_user.id,
                         "Сейчас глянем. Отправь трехбуквенный код или название города отправления (например, "
                         "MOW или Москва):",
                         reply_markup=keyboard)
        bot.register_next_step_handler(message, get_where_1)
    elif message.text == "А что по курсу валют?":
        get_currencies(message)
    else:
        menu(message)


def get_companies(message):
    if message.text and message.text == 'Назад':
        menu(message)
    else:
        if message.text == 'Аэрофлот':
            company = 'SU'
        elif message.text == 'S7 Airlines':
            company = 'S7'
        elif message.text == 'Победа':
            company = 'DP'
        elif message.text == 'Utair':
            company = 'UT'
        else:
            company = message.text
        result = api.getTopCompanies(company)
        if result:
            current = 1
            text = "Для выбранной авиакомпании следующие направления самые популярные: \n"
            for direction, popularity in result["data"].items():
                direction = direction.split('-')
                if direction[0] in AIRPORTS:
                    name1 = AIRPORTS[direction[0]]["name"]
                else:
                    name1 = CITIES[direction[0]]["name"]
                if direction[1] in AIRPORTS:
                    name2 = AIRPORTS[direction[1]]["name"]
                else:
                    name2 = CITIES[direction[1]]["name"]
                text += str(current) + '. ' + name1 + ' -> ' + name2 + '\n'
                current += 1
            bot.send_photo(message.from_user.id, "https://pics.avs.io/500/250/" + company + ".png", caption=text)
            bot.register_next_step_handler(message, get_companies)
        else:
            bot.send_message(message.from_user.id, "Наверное, такой авиакомпании не существует")
            bot.register_next_step_handler(message, get_companies)


def get_when_1(message):
    if message.text and message.text == 'Назад':
        menu(message)
    else:
        airport_from = ""
        name = ""
        if message.text in CITIES:
            airport_from = message.text
            name = CITIES[airport_from]["name"]
        elif next((code for code, city_item in CITIES.items() if city_item["name"] == message.text), None) is not None:
            airport_from = next((code for code, city_item in CITIES.items() if city_item["name"] == message.text), None)
            name = CITIES[airport_from]["name"]
        else:
            bot.send_message(message.from_user.id, "Что-то пошло не так")
            menu(message)
        if airport_from != "":
            keyboard = types.ReplyKeyboardMarkup(True, True)
            keyboard.add(types.KeyboardButton('Назад'))
            bot.send_message(message.from_user.id,
                             f"Окей, с городом отправления определились - {name}. Отправь трехбуквенный код или "
                             f"название города назначения (например, MOW или Москва):",
                             reply_markup=keyboard)
            bot.register_next_step_handler(message, get_when_2, airport_from)


def get_when_2(message, airport_from):
    if message.text and message.text == 'Назад':
        menu(message)
    else:
        airport_to = ""
        name = ""
        if message.text in CITIES:
            airport_to = message.text
            name = CITIES[airport_to]["name"]
        elif next((code for code, city_item in CITIES.items() if city_item["name"] == message.text), None) is not None:
            airport_to = next((code for code, city_item in CITIES.items() if city_item["name"] == message.text), None)
            name = CITIES[airport_to]["name"]
        else:
            bot.send_message(message.from_user.id, "Что-то пошло не так")
            menu(message)
        if airport_to != "":
            bot.send_message(message.from_user.id, f"Так, с городом назначения тоже - {name}. Ищу билеты...")
            name_from = CITIES[airport_from]["name"]
            data = api.getWhen(airport_from, airport_to)
            if data:
                text = "Так, самый дешевый вариант:\n\n"
                for variant in list(data["data"].values())[0].values():
                    text += str(variant["price"]) + " руб.\n" + 'Рейс ' + variant["airline"] + str(
                        variant["flight_number"]) + "\n" + "Вылет из г. " + name_from + ": " + dateutil.parser.isoparse(
                        variant["departure_at"]).strftime(
                        "%d.%m в %H:%M") + "\nПрилет обратно в г. " + name_from + ": " + dateutil.parser.isoparse(
                        variant["return_at"]).strftime("%d.%m в %H:%M") + "\n\n"
                    break
                bot.send_message(message.from_user.id, text)
                menu(message)
            else:
                bot.send_message(message.from_user.id, "Что-то пошло не так")
                menu(message)


def get_where_1(message):
    if message.text and message.text == 'Назад':
        menu(message)
    else:
        airport_item = ""
        name = ""
        if message.text in CITIES:
            airport_item = message.text
            name = CITIES[airport_item]["name"]
        elif next((code for code, city_item in CITIES.items() if city_item["name"] == message.text), None) is not None:
            airport_item = next((code for code, city_item in CITIES.items() if city_item["name"] == message.text), None)
            name = CITIES[airport_item]["name"]
        else:
            bot.send_message(message.from_user.id, "Что-то пошло не так")
            menu(message)
        if airport_item != "":
            keyboard = types.ReplyKeyboardMarkup(True, True)
            keyboard.add(types.KeyboardButton('Назад'))
            bot.send_message(message.from_user.id,
                             f"Окей, с городом отправления определились - {name}. Отправь дату отправления в формате "
                             f"YYYY-MM-DD:",
                             reply_markup=keyboard)
            bot.register_next_step_handler(message, get_where_2, airport_item)


def get_where_2(message, airport_item):
    if message.text and message.text == 'Назад':
        menu(message)
    else:
        keyboard = types.ReplyKeyboardMarkup(True, True)
        keyboard.add(types.KeyboardButton('Назад'))
        bot.send_message(message.from_user.id, f"Отправь дату прибытия в формате YYYY-MM-DD:", reply_markup=keyboard)
        bot.register_next_step_handler(message, get_where_3, airport_item, message.text)


def get_where_3(message, airport_item, datefrom):
    if message.text and message.text == 'Назад':
        menu(message)
    else:
        dateto = message.text
        bot.send_message(message.from_user.id, f"Ищу билеты...")
        variants = api.getWhere(airport_item, datefrom, dateto)
        if variants:
            text = "Так, лучшие направления:\n\n"
            for variant in variants["data"]:
                text += str(variant["price"]) + " руб.\n" + 'Рейс ' + variant["airline"] + str(
                    variant["flight_number"]) + "\n" + "Город " + CITIES[variant["destination"]][
                            "name"] + "\nВылет: " + dateutil.parser.isoparse(
                    variant["departure_at"]).strftime(
                    "%d.%m в %H:%M") + "\nПрилет: " + dateutil.parser.isoparse(
                    variant["return_at"]).strftime("%d.%m в %H:%M") + "\n\n"
            bot.send_message(message.from_user.id, text)
            menu(message)
        else:
            bot.send_message(message.from_user.id, "Что-то пошло не так")
            menu(message)


def get_often(message):
    if message.text and message.text == 'Назад':
        menu(message)
    else:
        airport_item = ""
        if message.location:
            latitude = message.location.latitude
            longitude = message.location.longitude
            data = [(math.sqrt((x["coordinates"]["lon"] - longitude) ** 2 + (x["coordinates"]["lat"] - latitude) ** 2),
                     code) if x["coordinates"] and x["coordinates"]["lat"] else (999999999, "")
                    for code, x in AIRPORTS.items()]
            data.sort()
            data = data[0]
            if data:
                airport_item = data[1]
                name = AIRPORTS[airport_item]["name"]
                bot.send_message(message.from_user.id,
                                 f"Я нашёл тебя!\n\nБлижайший аэропорт/вокзал к тебе - {name}.\n\n"
                                 f"Сейчас посмотрим, куда тебя отправить.")
            else:
                bot.send_message(message.from_user.id, "Что-то пошло не так")
                menu(message)
        elif message.text in AIRPORTS:
            airport_item = message.text
        elif next((code for code, airport_item in AIRPORTS.items() if airport_item["name"] == message.text),
                  None) is not None:
            airport_item = next(
                (code for code, airport_item in AIRPORTS.items() if airport_item["name"] == message.text), None)
        elif message.text in CITIES:
            airport_item = message.text
        elif next((code for code, city_item in CITIES.items() if city_item["name"] == message.text), None) is not None:
            airport_item = next((code for code, city_item in CITIES.items() if city_item["name"] == message.text), None)
        else:
            bot.send_message(message.from_user.id, "Что-то пошло не так")
            menu(message)

        data = api.getTopDirections(airport_item)
        if airport_item != "" and data:
            text = "Самые популярные направления для твоего города:\n\n"
            shown = 0
            for city_item in data["data"].values():
                if city_item["destination"] in AIRPORTS:
                    airport_item = AIRPORTS[city_item["destination"]]
                    name = CITIES[airport_item["city_code"]]["name"] + ", " + COUNTRIES[airport_item["country_code"]][
                        "name"] + '\nАэропорт ' + airport_item["name"]
                else:
                    airport_item = CITIES[city_item["destination"]]
                    name = CITIES[city_item["destination"]]["name"] + ", " + COUNTRIES[airport_item["country_code"]][
                        "name"] + '\nВсе аэропорты'
                text += name + "\n" + str(city_item["price"]) + " руб.\n\n"
                shown += 1
                if shown == 5:
                    break
            bot.send_message(message.from_user.id, text)
            menu(message)


def get_currencies(message):
    currencies = api.getCurrencies()
    if currencies:
        text = "А с валютой ситуация следующая:\n\nДоллар: " + str(round(currencies["usd"], 2)) + ' руб.\nЕвро: ' + str(
            round(currencies["eur"], 2)) + ' руб.'
        bot.send_message(message.from_user.id, text)
    else:
        bot.send_message(message.from_user.id, "Что-то пошло не так")
    menu(message)


bot.polling(none_stop=True, interval=0)
