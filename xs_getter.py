# _*_ coding: utf-8 _*_

"""
xs_getter is a scraper that takes the url of the index page of
a Chinese novel as its input, and outputs a text file with the complete
text of the novel.
"""
# TODO: Get rid of "->正文" with ->?\W\W, get rid of 努努书坊 版权所有,
# get rid of extra newlines

import re
import urllib2
from bs4 import BeautifulSoup

# This needs to be the url of the index page of novel.
url = raw_input("Please enter a URL:").replace("index.html", "")
response = urllib2.urlopen(url)
toc_html = response.read()

# Use regular expressions to find chapter codes in html
re_find_chapters = re.compile('(?<=><a href=")\d+(?=\.)')
chapter_codes = re_find_chapters.findall(toc_html)


# Create new urls
for code in chapter_codes:
    new_url = url + code + ".html"
    new_response = urllib2.urlopen(new_url)
    html = new_response.read()
    cleaner_html = re.sub('(?<=<a)|\n.*(?=</a)', '', html)
    soup = BeautifulSoup(cleaner_html)
    pro_soup = soup.get_text()
    cleaner_soup = re.sub('<!--.*-->', '', pro_soup, flags=re.DOTALL)

    # open new text file to fill with novel text
    with open("xiaoshuo.txt", 'a') as f:
        f.write(cleaner_soup.encode('utf-8'))
