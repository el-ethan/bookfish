# _*_ coding: utf-8 _*_
# TODO: Write docstrings
import re

try:
    import urllib2  # For compatibility with Python 2.X
    from urllib.request import urlopen
except ImportError:
    pass


class Bookfish():

    sites = {'nunu':{'junk': '<a.*?</a>'
                             '|<.*?>'
                             '|<!--(.*\n)+?-->'
                             '|&.*?;',
                    'tails': '(?<=<a href=")\d+.html?'},
            'hexun':{'junk': '<a.*?</a>'
                             '|\n(.*</script>)'
                             '|<.*?\s?>'
                             '|.*\}'
                             '|.*\{'
                             '|.*;'
                             '|<!--(.*\n)+?-->'
                             '|&.*?;'
                             '|src=.*'
                             '|<iframe.*'
                             '|//.*'
                             '|..onclick=.*',
                    'tails': '(?<=<a href="/)chapter[-\d\w]+.shtml'},
            'yanqing888':{'junk': '',
                    'tails': '(?<=<a href=")\d+.html'},
            'dddbbb':{'junk': '',
                      'tails': '(?<=<a href=")/\d+_\d+\.html'},
    }
    codec = 'gb18030'
    codecs = ['gb18030', 'gb2312', 'gbk', 'big5']
    fish = '¸.·´¯`·.´¯`·.¸¸.·´¯`·.¸><(((º>'

    def __init__(self, url):

        self.url = url
        self.site_name = ''
        for sn in self.sites.keys():
            if sn in self.url:
                self.site_name = sn
        self.html = self.get_html(self.url)
        self.title = self.get_title()
        self.html_book = self.get_html_book()
        self.book = self.get_book()

    def codec_generator(self):
        for codec in self.codecs:
            yield codec

    def get_html(self, url):
        codec = self.codec_generator()
        while True:
            try:
                html = urlopen(url).read().decode(next(codec))
                break
            except UnicodeDecodeError:
                continue
        return html

    def get_title(self):
        re_find_title = re.search('(?<=<title>).*(?=</title>)', self.html)
        title = re_find_title.group()
        return title

    def get_html_book(self):
        re_find_tails = re.compile(self.sites[self.site_name]['tails'])
        url_tails = re_find_tails.findall(self.html)
        # Get html of novel
        html_book = ''
        for tail in url_tails:
            url_base = re.sub('\.html?$'            # nunu, yanqing888
                              '|book-\d+.shtml'     # hexun
                              '|/html/.*opf.html',  # dddbbb
                              '', self.url)
            new_url = url_base + tail
            html = self.get_html(new_url)
            html_book += '#'*20 + html
        return html_book

    def get_book(self):
        text = re.sub(self.sites[self.site_name]['junk'], '', self.html_book)
        # self.site_name specific junk to remove
        leftover_junk = {'nunu': ['--正文', '努努书坊 版权所有','|'
                     ],
                     'hexun': ['if(w_frame.readyState)', 'else', '*/', '/*'
                     ],
                     'dddbbb': ['|', '>']
        }
        # Extra newlines (2 or more consecutive)
        extra_lines = re.compile('\s{2,}')
        # Remove self.site_name specific junk from text
        for j in leftover_junk[self.site_name]:
            text = text.replace(j, '')
        # Remove extra whitespace
        text = re.sub(extra_lines, '\n\n', text)
        # text += '\n' + u'\U0001F41F'*20
        return text

    def make_file(self):
        with open("%s.txt" % self.title, 'ab') as f:
            f.write(self.book.encode('utf-8'))

    def get_fish(self):
        return self.fish


class TwoFish(Bookfish):
    fish = '><(((º>TwoFish<º)))><'

    def get_html(self, url):
        codec = self.codec_generator()
        while True:
            try:
                html = urllib2.urlopen(url).read().decode(next(codec))
                break
            except UnicodeDecodeError:
                continue
        return html

# if __name__ == "__main__":
#     url = input("Enter a URL:")
#     if not url:
#         url = 'http://data.book.hexun.com/book-19250.shtml'
#     print(bookfish(url))

# novel = Bookfish('http://data.book.hexun.com/book-19250.shtml')
# print(novel.url)
# print(novel.site_name)
# print(novel.fishy())
# # print(novel.get_html())
# print(novel.get_title())
# print(novel.book)