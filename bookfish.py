#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
"""Bookfish"""
import re
import urllib.request


class Bookfish(object):

    def __init__(self, url):
        self.url = url
        self.html = self.get_html()
        self.chapters = self.find_chapter_urls()

    def get_html(self):
        f = urllib.request.urlopen(self.url)
        html = f.read()
        html = html.decode('gb18030')
        return html

    def find_chapter_urls(self):
        """Take url and return chapters"""
        regex = re.compile(r'(?<=href=")\d+\.html')
        m = re.findall(regex, self.html)
        chapter_urls = []
        for chapter in m:
            chapter_urls.append(self.url + chapter)
        return chapter_urls


if __name__ == '__main__':
    url = 'http://www.kanunu8.com/book3/7192/'
    fish = Bookfish(url)
    print(fish.chapters)