import logging
from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import urllib3 as urllib
import xmltodict
import urllib.request as urllib
import xmltodict
from conda_env import yaml
from _datetime import datetime, timedelta




app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

def parse():
    file = urllib.urlopen('https://www.morgenweb.de/feed/201-alexa-advanced-mm-startseite.xml')
    data = file.read()
    file.close()

    data = xmltodict.parse(data)
    return data
def get_day(day):
    now = datetime.now()
    abbreviation = now.strftime("%a")
    abb = 'Sat'
    if (day == 'heute'):
        abb = abbreviation
    elif (day == 'gestern'):
        now = now - timedelta(days=1)
        abb = now.strftime("%a")
    elif (day == 'samstag'):
        abb = 'Sat'
    elif (day == 'sonntag'):
        abb = 'Sun'
    elif (day == 'montag'):
        abb = 'Mon'
    elif (day == 'dienstag'):
        abb = 'Tue'
    elif (day == 'mittwoch'):
        abb = 'Wed'
    elif (day == 'dienstag'):
        abb = 'Thu'
    elif (day == 'freitag'):
        abb = 'Fri'

    return abb


@ask.launch

def new_session():

    welcome_msg = render_template('welcome')
    return question(welcome_msg)

@ask.intent("NewsIntent")

def get_news(day):

    data = parse()
    day1 = get_day(day)
    # len = len(data['rss']['channel']['item'])  # [4]['description'])
    len = 40
    i=0
    for elem in range(0, len):
        abb = data['rss']['channel']['item'][elem]['pubDate']
        if (day1==abb[0:3]):
            if (i==0) :
                description1 = data['rss']['channel']['item'][elem]['description']
                i = i + 1
                continue
            if (i==1) :
                description2 = data['rss']['channel']['item'][elem]['description']
                i = i + 1
                continue
            if (i==2) :
                description3 = data['rss']['channel']['item'][elem]['description']
                i = i + 1
                break

    news_msg = render_template('news', day=day, description1=description1, description2=description2, description3=description3)
    return statement(news_msg)

# @ask.intent("YesIntent")
#
# def next_round():
#
#     numbers = [randint(0, 9) for _ in range(3)]
#
#     round_msg = render_template('round', numbers=numbers)
#
#     session.attributes['numbers'] = numbers[::-1]  # reverse
#
#     return question(round_msg)


# @ask.intent("AnswerIntent", convert={'first': int, 'second': int, 'third': int})
#
# def answer(first, second, third):
#
#     winning_numbers = session.attributes['numbers']
#
#     if [first, second, third] == winning_numbers:
#
#         msg = render_template('win')
#
#     else:
#
#         msg = render_template('lose')
#
#     return statement(msg)


if __name__ == '__main__':

    app.run(debug=True)