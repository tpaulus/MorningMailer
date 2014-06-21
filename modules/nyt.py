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
        string = '%s\n\t%s\n\tImage: %s\n\tLink: %s\n' % (self.title, self.content, self.image, self.url)
        return string


class TopStories(object):
    key = Property.nyt_api_key

    def __init__(self):
        self.articles = []

    def pull(self, num):
        """Go fetch the paper boy!"""
        try:
            url = 'http://api.nytimes.com/svc/news/v3/content/nyt/u.s..json?&api-key=' + TopStories.key
            package = Requests.get(url)
            newspaper = package.json()

        except:
            return False

        for article in newspaper['results']:
            if len(self.articles) < num:
                title = article['title']
                content = article['abstract']
                source_url = article['url']
                img_url = ''
                if title.lower().find('briefing') != -1:
                    continue
                for media_num in range(len(article['multimedia'])):
                    if article['multimedia'][media_num]['format'] == 'Normal':
                        img_url = article['multimedia'][media_num]['url']
                        break
                if img_url == '':
                    continue
                new_article = Article(title, content, img_url, url)
                self.articles.append(new_article)

        return self.articles
    def get(self, num):
        self.pull(num)
        return self.articles


if __name__ == '__main__':
    news = TopStories()
    for a in news.get(4):
        print str(a)