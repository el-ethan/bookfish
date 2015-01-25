# _*_ coding: utf-8 _*_
# TITLE: xiaoshuo_extractor v2.0 2014-12-25
# TODO: write something that removes index.html from url of index if that exists

"""
xs_getter is a scraper that takes the url of for the index page of
a Chinese novel as its input, and outputs a text file with the complete
text of the novel.
"""

import re
import urllib2
from bs4 import BeautifulSoup

# Get html of index page
url = raw_input("Please enter a URL:").replace("index.html", "")
response = urllib2.urlopen(url)
toc_html = response.read()

# Use regular expressions to find chapter codes in html
re_find_chapters = re.compile('(?<=><a href=")\d+(?=\.)')
chapter_codes = re_find_chapters.findall(toc_html)

# Create new urls
for code in range(0, len(chapter_codes)):
    new_url = url + chapter_codes[code] + ".html"
    new_response = urllib2.urlopen(new_url)
    html = new_response.read()
    cleaner_html = re.sub('(?<=<a)|\n.*(?=</a)', "", html)
    soup = BeautifulSoup(cleaner_html)
    pro_soup = soup.get_text()
    # TODO: Get rid of "->正文" with ->?\W\W, get rid of 努努书坊 版权所有,
    # get rid of extra newlines
    cleaner_soup = re.sub('<!--.*-->', "", pro_soup, flags = re.DOTALL)


    # open new text file to fill with novel text
    with open("xiaoshuo.txt", 'a') as f:
        f.write(cleaner_soup.encode('utf-8'))