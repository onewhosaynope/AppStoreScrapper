import json
import data
from telebot import TeleBot
from time import sleep
from datetime import datetime, timedelta
from helpers import bcolors
from scrapper import scrap


def scrap_and_save():
    print("\n" + bcolors.WARNING + "BEGINNING SCRAPING" + bcolors.ENDC + "\n")

    with open("results.json", "r") as read_file:
        results = json.load(read_file)
        read_file.close()

    result_ru = scrap(data.link_ru)
    result_us = scrap(data.link_us)

    for item in result_us:
        if item not in result_ru:
            result_ru.append(item)
    
    for item in result_ru:
        if item not in results:
            results.append(item)

    print("items in \"RESULTS.JSON\": ")
    print(bcolors.HEADER + str(len(results)) + bcolors.ENDC)

    with open('results.json', 'w') as file_output:
        json.dump(results , file_output)
        print('saved results')
        file_output.close()

    print("\n" + bcolors.OKGREEN + "DONE" + bcolors.ENDC + "\n")


def clean_json():

    print("\n" + bcolors.WARNING + bcolors.BOLD + "CLEANING RESULTS" + bcolors.ENDC + "\n")

    clean_list = []
    with open('results.json', 'w') as file_output:
        json.dump(clean_list , file_output)
        file_output.close()
    print("\"RESULTS.JSON\" is empty now")

    print("\n" + bcolors.OKGREEN + "DONE" + bcolors.ENDC + "\n")


def send_results():

    print("\n" + bcolors.WARNING + "SENDING RESULTS" + bcolors.ENDC + "\n")

    with open("results.json", "r") as read_file:
        jdata = json.load(read_file)

    botToken = data.token
    bot = TeleBot(botToken)
    bot.config['api_key'] = botToken
    print(bot.get_me())
    scrp_date = (datetime.now()-timedelta(days=1)).strftime("%d %B")
    bot.send_message(data.channel_ru, "Releases of: " + scrp_date)
    
    count = 0
    for i in jdata:
        count = count + 1
        message = "Title:\n" + i.get("title") + "\n\nCategory:\n" + i.get("category") + "\n\nPrice:\n" + i.get("cost") + "\n\nLink RU:\n" + i.get("app_link_ru") + "\n\nLink US:\n" + i.get("app_link_us") + "\n\nAuthor:\n" + i.get("author") + "\n\nAuthor Link RU:\n" + i.get("author_link_ru") + "\n\nAuthor Link US:\n" + i.get("author_link_us")
        bot.send_message(data.channel_ru, message)
        sleep(0.5)
    bot.send_message(data.channel_ru, "Totall apps: " + str(count))
    print("Totall apps for " + scrp_date + ":")
    print(bcolors.HEADER + str(count) + bcolors.ENDC)

    print("\n" + bcolors.OKGREEN + "DONE" + bcolors.ENDC + "\n")

