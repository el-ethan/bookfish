#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
"""
Bookfish crawls through Chinese novel websites and gives you the novels in plain
text.
"""
import re
import urllib.request


class Bookfish(object):
    """Bookfish objects are passed a url of an index page for a Chinese novel
    and will give you the text of that novel as a plain text string, or if
    print_to_file is set to True, will print the contents of the novel to a
    file the title of which should match the pattern title_author.
    """

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
        """Return html of url"""
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
        """Return title of novel and author"""
        regex = re.compile(r'(?<=<title>)(.*?)\s-\s(.*?)(?=\s-.*</title>)')
        m = regex.search(self.html)
        return m.groups()

    def get_book(self):
        """Return text of novel"""
        html = ''
        # Unicode fish character used as chapter separator
        ascii_fish ="><(((('>"
        for chapter in self.chapters:
            html += (ascii_fish) + self.get_html(chapter)

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
    test_url = input("Enter a URL or press return: ")
    if not test_url:
        test_url = 'http://www.kanunu8.com/book3/7192/'
    fish = Bookfish(test_url)
    print(fish.book)
