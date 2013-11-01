#! /usr/bin/python
# Written By Tom Paulus, @tompaulus, www.tompaulus.com

from __future__ import unicode_literals
import random


class Parse(object):
    def __init__(self):
        self.location = "./good_morning.csv"
        self.index = {}
        self.keys = []

    def file_len(self):
        """

        :return: the length of the file (int)
        """
        with open(self.location) as f:
            length = 0
            for _, l in enumerate(f):
                length += 1
        return length

    def get(self):
        f_len = self.file_len()
        with open(self.location) as data:
            for l in range(0, f_len):
                line = unicode(data.readline(), "utf-8").replace('"', '')
                info = line.split(',')
                name = info[0].strip()
                phrase = info[-1].strip()
                self.index[name] = phrase

        self.keys = list(self.index.keys())

    def get_dict(self):
        return self.index

    def get_random(self):
        key = random.choice(self.keys)
        phrase = self.index[key]
        return key, phrase

    def __str__(self):
        result = '{'
        for i in range(0, len(self.index)):
            key = self.keys[i]
            phrase = self.index[key]
            line = '"' + key + '" : "' + phrase + '",\n'
            line = line
            result += line
        result += '}'
        return result


if __name__ == '__main__':
    p = Parse()
    p.get()
    print p.get_random()