#! /usr/bin/python
# Written By Tom Paulus, @tompaulus, www.tompaulus.com

import sys

import lib.requests as Requests
from properties import Property

reload(sys)
sys.setdefaultencoding("utf-8")


class Article(object):
    def __init__(self, title, content, image, url):
        self.title = title
        self.content = content
        self.image = image
        self.url = url

    def __str__(self):
        return self.title + '\n\t' + self.content + '\n\tI:' + self.image + '\n\tL:' + self.url


class TopStroies(object):
    key = Property.nyt_api_key

    def __init__(self):
        self.articles = []

    def pull(self, num):
        url = 'http://api.nytimes.com/svc/news/v3/content/nyt/u.s..json?&api-key=' + TopStroies.key
        newspaper = Requests.get(url).json()
        for article_number in range(len(newspaper['results'])):
            if len(self.articles) < num:
                title = newspaper['results'][article_number]['title']
                content = newspaper['results'][article_number]['abstract']
                source_url = newspaper['results'][article_number]['url']
                img_url = ''
                for media_num in range(len(newspaper['results'][article_number]['multimedia'])):
                    if newspaper['results'][article_number]['multimedia'][media_num]['format'] == 'Normal':
                        img_url = newspaper['results'][article_number]['multimedia'][media_num]['url']
                        break
                if img_url == '':
                    continue
                new_article = Article(title, content, img_url, url)
                self.articles.append(new_article)

    def get(self, num):
        self.pull(num)
        return self.articles


if __name__ == '__main__':
    news = TopStroies()
    news.get(4)