#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
"""Bookfish"""
import re
import urllib.request


class Bookfish(object):

    def __init__(self, url):
        self.url = url
        self.html1 = self.get_html(self.url)
        self.chapters = self.find_chapter_urls()
        self.title = self.get_title_author()[0]
        self.author = self.get_title_author()[1]

    def get_html(self, url):
        f = urllib.request.urlopen(url)
        html = f.read()
        html = html.decode('gb18030')
        return html

    def find_chapter_urls(self):
        """Take url and return chapters"""
        regex = re.compile(r'(?<=href=")\d+\.html')
        m = re.findall(regex, self.html1)
        chapter_urls = []
        for chapter in m:
            chapter_urls.append(self.url + chapter)
        return chapter_urls

    def get_title_author(self):
        regex = re.compile(r'(?<=<title>)(.*?)\s-\s(.*?)(?=\s-.*</title>)')
        m = regex.search(self.html1)
        return m.groups()





if __name__ == '__main__':
    url = 'http://www.kanunu8.com/book3/7192/'
    fish = Bookfish(url)
    print(fish.chapters)