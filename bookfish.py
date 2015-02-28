# _*_ coding: utf-8 _*_
"""
><(((º>Bookfish
Bookfish is a tool for extracting Chinese novels from html.

This is useful if you don't want to read in the distracting
browser environment littered with pop-ups.

This module contains the class Bookfish(), which takes a URL
of a novel index/table of contents page as its only argument.
it will subsequently get the html from all the chapters of the
novel, remove html tags and some other extraneous text, and
return a more readable version of the novel. Options are available
to save the text to a file.

Currently, Bookfish is customized to work with novels hosted on
particular sites.

Supported sites:
* kanunu8.com
* yanqing888.com
* hexun.com
* dddbbb.net

><(((º>TwoFish<º)))><
The module also includes TwoFish, a subclass of Bookfish, which will
function with Python 2.7. All methods are inherited from Bookfish,
except the get_html method which is overridden by TwoFish and uses
urllib2.urlopen() to retrieve html instead of urllib.request.urlopen()
"""

import re
try:
    from urllib.request import urlopen
except ImportError:
    import urllib2  # For compatibility with Python 2.X


class Bookfish():
    """Bookfish creates a readable text representation of novel from html

    Feed Bookfish the URL of index/Table of contents page for a Chinese
    novel from a supported site. The resulting Bookfish object has the
    following methods and attributes:

    * html_book: the raw html of the entire novel
    * title: the title of the novel (this is used as the file name when
      make_file() is called)
    * url: the original url of index page
    * book: the complete text of the novel

    Also, you can call the object's make_file() method to save the novel into
    a txt file in the cwd. The name of the file will be the same as the
    object's title attribute.
    """
    sites = {'nunu':{'junk': '<a.*?</a>'
                             '|<.*?>'
                             '|<!--(.*\n)+?-->'
                             '|&.*?;',
                    'extens': '(?<=<a href=")\d+.html?'},
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
                    'extens': '(?<=<a href="/)chapter[-\d\w]+.shtml'},
            'yanqing888':{'junk': '',
                    'extens': '(?<=<a href=")\d+.html'},
            'dddbbb':{'junk': '',
                      'extens': '(?<=<a href=")/\d+_\d+\.html'},
    }

    codecs = ['gb18030', 'gb2312', 'gbk', 'big5']

    def __init__(self, url):
        self.url = url
        self.site_name = ''
        for sn in self.sites.keys():
            if sn in self.url:
                self.site_name = sn             # Name of source site
        self.html = self.get_html(self.url)     # HTML of index/TOC page
        self.title = self.get_title()           # Title of novel
        self.html_book = self.get_html_book()   # HTML of entire novel
        self.book = self.get_book()             # Full text of novel

    def codec_generator(self):
        """Generate codecs to decode Chinese text in html"""
        for codec in self.codecs:
            yield codec

    def get_html(self, url):
        """Get html from url and decode Chinese text"""
        codec = self.codec_generator()
        while True:
            try:
                html = urlopen(url).read().decode(next(codec))
                break
            except UnicodeDecodeError:
                continue
        return html

    def get_title(self):
        """Return title of novel with regex"""
        re_find_title = re.search('(?<=<title>).*(?=</title>)', self.html)
        title = re_find_title.group()
        return title

    def get_html_book(self):
        """Return html of complete novel with regex"""
        # Use regex to determine extensions at end of url (html, shtml, etc.)
        re_find_extens = re.compile(self.sites[self.site_name]['extens'])
        url_extens = re_find_extens.findall(self.html)
        # Combine url elements to form urls for each chapter
        html_book = ''
        for tail in url_extens:
            # Determine what needs to be stripped from end of url to make base
            url_base = re.sub('\.html?$'            # nunu, yanqing888
                              '|book-\d+.shtml'     # hexun
                              '|/html/.*opf.html',  # dddbbb
                              '', self.url)
            new_url = url_base + tail
            html = self.get_html(new_url)
            # Add row of 20 hash signs between chapters
            html_book += '#'*20 + html
        return html_book

    def get_book(self):
        """Return full text of novel by cleaning up html with regex"""
        # Remove html tags and extraneous text from html
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
        return text

    def make_file(self):
        with open("%s.txt" % self.title, 'ab') as f:
            f.write(self.book.encode('utf-8'))


class TwoFish(Bookfish):
    """TwoFish creates text representation of novel from html with Python 2.7

    Use this class if you are using Python 2.X. Otherwise use Bookfish
    for 3.X. Feed TwoFish the URL of index/Table of contents page for a
    Chinese novel from a supported site. The resulting TwoFish object
    has the following methods and attributes:

    * html_book: the raw html of the entire novel
    * title: the title of the novel (this is used as the file name when
      make_file() is called)
    * url: the original url of index page
    * book: the complete text of the novel

    Also, you can call the object's make_file() method to save the novel into
    a txt file in the cwd. The name of the file will be the same as the
    object's title attribute.
    """
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
