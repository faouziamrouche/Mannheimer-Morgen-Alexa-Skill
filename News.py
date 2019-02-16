import logging
from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import urllib3 as urllib
import xmltodict
import urllib.request as urllib
import xmltodict
from conda_env import yaml



app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

def parse():
    file = urllib.urlopen('https://www.morgenweb.de/feed/201-alexa-advanced-mm-startseite.xml')
    data = file.read()
    file.close()

    data = xmltodict.parse(data)
    return data

def parse():
    file = urllib.urlopen('https://www.morgenweb.de/feed/201-alexa-advanced-mm-startseite.xml')
    data = file.read()
    file.close()

    data = xmltodict.parse(data)
    return data

@ask.launch

def new_session():

    welcome_msg = render_template('welcome')

    return question(welcome_msg)

@ask.intent("NewsIntent")

def get_news(day):


    data = parse()
    description = data['rss']['channel']['item'][4]['description']
    news_msg = render_template('news', day=day, description=description)
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