#! /usr/bin/python
# Written By Tom Paulus, @tompaulus, www.tompaulus.com

from __future__ import unicode_literals
import os
import random
from modules.parse import Greeting
from modules.SendEmail import *
from modules.wunderground import *
from modules.todoist import *
from modules.nyt import *
from modules.properties import Property


def greeting():
    p = Greeting()
    p.get()
    return p.get_random()


def weather():
    w = Weather(Property.user_city, Property.user_state)
    w.get_data()
    text, icon = w.get_forecast()
    map_URL = w.get_map_url()
    download(Property.weather_url, "radar.gif", map_URL)
    return text, icon


def todo():
    t = Todos(Property.todoist_email, Property.todoist_password)
    task_list = t.get()
    section = '<ul>'
    for task in task_list:
        due = datetime.strftime(task.due, '%a %b %d, %Y')
        text = task.name + ', Due: ' + due + ' - ' + task.project
        # TODO fix usage of deprecated <font> tag
        if task.priority == 4:
            line = '<font color="#B8412B">' + text + '</font>'
        elif task.priority == 3:
            line = '<font color="#3363A4">' + text + '</font>'
        elif task.priority == 2:
            line = '<font color="#8EC4FF">' + text + '</font>'
        else:
            line = text

        line = '<li>' + line + '</li>\n'
        section += line

    section += '</ul>'
    return section
    # TODO Add tags to list as sub elements
    # The <dl> tag is used in conjunction with <dt> (defines terms/names) and <dd> (describes each term/name)


def news():
    news = TopStroies()
    articles = news.get(4)
    for num in range(len(articles)):
        download(Property.news_url, str(num + 1) + ".jpg", articles[num].image)
    return articles


def send(message):
    email = mail()
    if email.send(Property.email_to, Property.email_subject, message):
        pass
    else:
        quit("Mail Send Error")


def download(path, name, url):
    save_location = Property.root_path + path + name
    wget = "wget -qO " + save_location + " " + url
    chmod = "chmod 644 " + save_location
    if Property.on_server:
        os.system(wget)
        os.system(chmod)


template_loc = './email_template.html'
result_loc = './email.html'

header_image = '<img src="' + Property.root_web_path + Property.header_url + '{0}.jpg"  style="max-width: 600px;' \
    ' id="headerImage" mc:label="header_image" mc:edit="header_image" mc:allowdesigner mc:allowtext/>'.format(
    random.randint(0, 10))

language, greeting = greeting()
date = datetime.now().strftime("%A, %B %d, %Y")

weather_text, weather_icon = weather()

article_list = news()

html_tag_index = {
    '<python id="image-header"/>': header_image,
    '<python id="header"/>': greeting + ", that's " + language + ' for Good Morning!',
    '<python id="date"/>': 'Today is ' + date + '.',
    '<python id="weather-text"/>': 'It will be ' + weather_text,
    '<python id="tasks"/>': todo(),
    '<python id="news-1-headline"/>': article_list[0].title,
    '<python id="news-1-body"/>': article_list[0].content,
    '<python id="news-2-headline"/>': article_list[1].title,
    '<python id="news-2-body"/>': article_list[1].content,
    '<python id="news-3-headline"/>': article_list[2].title,
    '<python id="news-3-body"/>': article_list[2].content,
    '<python id="news-4-headline"/>': article_list[3].title,
    '<python id="news-4-body"/>': article_list[3].content
}

with open(template_loc, 'r') as template:
    message = template.read()

for i in range(0, len(list(html_tag_index.keys()))):
    tag = str(list(html_tag_index)[i])
    replacement = str(html_tag_index[tag])
    message = message.replace(tag, replacement)

send(message)

email = open(result_loc, 'w')
email.write(message)
email.close()
