import requests
from bs4 import BeautifulSoup
from datetime import date, datetime
import datetime
import re

debug_mode = 0


def debug(message=None):
    if debug_mode == 1:
        print(message)


CLEANR = re.compile('<.*?>')


def cleanhtml(raw_html):
    cleantext = re.sub(CLEANR, '', raw_html)
    return cleantext


def cleanspacec(raw_text):
    cleantext = re.sub(' +', ' ', raw_text)

    cleantext = cleantext.replace('Observações: ', '')

    return cleantext


def get_menu(today=date.today().strftime("%Y-%m-%d")):
    URL = "https://www.prefeitura.unicamp.br/apps/cardapio/index.php?d="
    URL_d = URL + today
    #  print(URL_d)

    page = requests.get(URL_d)
    meal = []

    soup = BeautifulSoup(page.content, "html.parser")

    if soup.__str__().find('Não existe cardápio cadastrado no momento') == 1:
        return {}
    meals = soup.findAll("div", class_="menu-item-name")
    sides = soup.findAll("div", class_="menu-item-description")
    count = 0

    meal = {}
    day = []

    for i in range(0, 4):

        meal['date'] = today
        meal['main_dish'] = cleanhtml(meals[i].__str__())
        if i in [1, 3]:
            meal['veg'] = 1
        else:
            meal['veg'] = 0

        if i in [0, 1]:
            meal['lunch'] = 1
        else:
            meal['lunch'] = 0

        texto = cleanspacec(cleanhtml((sides[i].__str__().replace('<br/>', '\n'))))
        text = texto.splitlines()
        meal['salad'] = text[3]
        meal['dessert'] = text[4]
        meal['side'] = text[1]
        # print(meal)
        day.append(meal.copy())
    #        print(meal['main_dish'])
    #        print(meal['side'])
    #        print(meal['salad'])
    #        print(meal['dessert'])
    #

    return day


def _getMonday():
    today = date.today()
    monday = today - datetime.timedelta(days=today.weekday())
    return monday


def _getFriday():
    monday = _getMonday() + datetime.timedelta(4)
    return monday


def getWeek():
    week = []
    aux = []
    start_date = _getMonday()
    end_date = _getFriday()
    delta = datetime.timedelta(days=1)
    while start_date <= end_date:
        # print(start_date.strftime("%Y-%m-%d"))
        aux = get_menu(start_date.strftime("%Y-%m-%d"))
        # print(aux)
        for m in aux:
            week.append(m)
        start_date += delta
    return week

# print(getWeek())
