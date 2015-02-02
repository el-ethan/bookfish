"""
bookworm is a scraper that takes the url of the index page of
a Chinese novel as its input, and outputs a text file with the complete
text of the novel.

Currently the url should be from 努努书坊.
"""
import re
from urllib.request import urlopen
import fishfood


def html_decoder(html, codec):
    """decode html and return string"""
    html = html.decode(codec)
    return str(html)

# Get html of index page of novel
url =  'http://www.kanunu8.com/book3/7192/'     # For testing purposes
# input("Please enter a URL:").replace("index.html", "")
response = urlopen(url)
html = response.read()
html = html_decoder(html, codec='gb18030')

# Use regex to find chapter codes in html, save as list
re_find_chapters = re.compile('(?<=><a href=")\d+(?=\.)')
chapter_codes = re_find_chapters.findall(html)

# Find title in html to use as output file name
m = re.search('(?<=<title>).*(?=</title>)', html)
title = m.group()

# Create new urls
for code in chapter_codes:
    new_url = url + code + ".html"
    new_response = urlopen(new_url)
    html = new_response.read()
    html = html_decoder(html, codec='gb18030')

    # Remove extraneous text that get_text below doesn't remove
    text = fishfood.html_clnr(html, site='nunu')

    # open new text file to fill with novel text
    with open("%s.txt" % title, 'ab') as f:
        f.write(text.encode('utf-8'))
