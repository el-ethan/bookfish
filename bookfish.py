# TODO: Write docstrings
import re
from urllib.request import urlopen

class Bookfish():

    fish = '¸.·´¯`·.´¯`·.¸¸.·´¯`·.¸><(((º>'
    fish2 = u"\U0001F41F Thanks for using Bookfish!"
    fish3 = u"\U0001F41F" * 20
    fish4 = "\U0001F41F" * 20
    site_names = ['nunu', 'yanqing888', 'hexun', 'dddbbb']
    codec = 'gb18030'

    def __init__(self, url):

        self.url = url
        self.site_name = ''
        for sn in self.site_names:
            if sn in self.url:
                self.site_name = sn
        self.html = self.get_html()
        self.title = self.get_title()
        self.html_book = self.get_html_book()
        self.book = self.get_book()

    def get_html(self):
        html = urlopen(self.url).read().decode(self.codec)
        return html

    def get_title(self):
        re_find_title = re.search('(?<=<title>).*(?=</title>)', self.html)
        title = re_find_title.group()
        return title

    def get_html_book(self):
        # Get chapters
        if self.site_name == 'nunu':
            re_find_tails = re.compile('(?<=<a href=")\d+.html?')
        elif self.site_name == 'yanqing888':
            re_find_tails = re.compile('(?<=<a href=")\d+.html')
        elif self.site_name == 'hexun':
            re_find_tails = re.compile('(?<=<a href="/)chapter[-\d\w]+.shtml')
        elif self.site_name == 'dddbbb':
            re_find_tails = re.compile('(?<=<a href=")/\d+_\d+\.html')

        url_tails = re_find_tails.findall(self.html)
        # Get html of novel
        html_book = ''
        for tail in url_tails:
            url_base = re.sub('\.html?$'            # nunu, yanqing888
                              '|book-\d+.shtml'     # hexun
                              '|/html/.*opf.html',  # dddbbb
                              '', self.url)
            new_url = url_base + tail
            html = urlopen(new_url).read().decode(self.codec)
            html_book += '#'*20 + html
        return html_book

    def get_book(self):
        if self.site_name == 'nunu':
            text = re.sub('<a.*?</a>'
                          '|<.*?>'
                          '|<!--(.*\n)+?-->'
                          '|&.*?;', '', self.html_book)
        elif self.site_name == 'hexun' or self.site_name == 'dddbbb':
            text = re.sub('<a.*?</a>'
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
                          '|..onclick=.*', '', self.html_book)
        # self.site_name specific junk to remove
        site_junk = {'nunu': ['--正文', '努努书坊 版权所有','|'
                     ],
                     'hexun': ['if(w_frame.readyState)', 'else', '*/', '/*'
                     ],
                     'dddbbb': ['|', '>']
        }
        # Extra newlines (2 or more consecutive)
        extra_lines = re.compile('\s{2,}')
        # Remove self.site_name specific junk from text
        for junk in site_junk[self.site_name]:
            text = text.replace(junk, '')
        # Remove extra whitespace
        text = re.sub(extra_lines, '\n\n', text)
        text += '\n' + u'\U0001F41F'*20
        return text

    def make_file(self):
        with open("%s.txt" % self.title, 'ab') as f:
            f.write(self.book.encode('utf-8'))

    def fishy(self):
        return self.fish

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