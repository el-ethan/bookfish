#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
"""Bookfish"""
import re
import urllib.request


class Bookfish(object):

    def __init__(self, url, print_to_file=False):
        self.url = url
        self.html = self.get_html(self.url)
        self.chapters = self.find_chapter_urls()
        self.title = self.get_title_author()[0]
        self.author = self.get_title_author()[1]
        self.book = self.get_book()
        self.charcount = len(self.book.strip())

        if print_to_file:
            filename = '{0}_{1}.txt'.format(self.title, self.author)
            with open(filename, 'w') as f:
                f.write(self.book)

    def get_html(self, url):
        f = urllib.request.urlopen(url)
        html = f.read()
        html = html.decode('gb18030')
        return html

    def find_chapter_urls(self):
        """Take url and return chapters"""
        regex = re.compile(r'(?<=href=")\d+\.html')
        m = re.findall(regex, self.html)
        chapter_urls = []
        for chapter in m:
            chapter_urls.append(self.url.rstrip('index.html') + chapter)
        return chapter_urls

    def get_title_author(self):
        regex = re.compile(r'(?<=<title>)(.*?)\s-\s(.*?)(?=\s-.*</title>)')
        m = regex.search(self.html)
        return m.groups()

    def get_book(self):
        html = ''
        # Unicode fish character used as chapter separator
        fish_char = u'\U0001F41F'
        for chapter in self.chapters:
            html += (fish_char) + self.get_html(chapter)

        regex = re.compile(r"""
                           <a.*?</a>        # Links
                           |<.*?>           # HTML tags
                           |-?&.*?;         # HTML entities
                           |\|              # Pipes
                           |\s{3,}          # Empty space
                           |<!--.*?-->      # HTML comments
                           """, re.VERBOSE | re.DOTALL)
        regex_site_specific = re.compile(r"""
                                        正文\s
                                        |业务QQ:\s\d+
                                        |\s小说在线阅读\s
                                        |努努书坊\s版权所有
                                         """, re.VERBOSE)

        book = re.sub(regex, '', html)
        book = re.sub(regex_site_specific, '', book)

        return book

if __name__ == '__main__':
    url = input("Enter a URL or press return: ")
    if not url:
        url = 'http://www.kanunu8.com/book3/7192/'
    fish = Bookfish(url)
    print(fish.book)