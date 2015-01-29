"""
xs_getter is a scraper that takes the url of the index page of
a Chinese novel as its input, and outputs a text file with the complete
text of the novel.

Currently the url should be from 努努书坊.
"""
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup

def html_fixer(html, codec):
    """decode html and return string"""
    html = html.decode(codec)
    return str(html)

# Get html of index page of novel
url =  'http://www.kanunu8.com/book4/9781/'
# input("Please enter a URL:").replace("index.html", "")
response = urlopen(url)
html = response.read()
html = html_fixer(html, 'gb18030')

# Use regex to find chapter codes in html, save as list list
re_find_chapters = re.compile('(?<=><a href=")\d+(?=\.)')
chapter_codes = re_find_chapters.findall(html)

# Find title in html
m = re.search('(?<=<title>).*(?=</title>)', html)
title = m.group()

# Use regex to find extraneous text and code to be removed later
junk = re.compile('(?<=<a)|\n.*(?=</a)')
html_comm = re.compile('<!--.*-->', flags=re.DOTALL)
extra_lines = re.compile('\n{4,}')

# Create new urls and make soup
for code in chapter_codes:
    new_url = url + code + ".html"
    new_response = urlopen(new_url)
    html = new_response.read()
    html = html_fixer(html, 'gb18030')
    # Remove extraneous text that get_text below doesn't remove
    clean_html = re.sub(html_comm, '', html)
    cleaner_html = re.sub(junk, '', clean_html)
    soup = BeautifulSoup(cleaner_html)
    text = soup.get_text()

    # Clean up text
    rm_lines = re.sub(extra_lines, '\n\n', text)
    clean_text = rm_lines.replace(u'->正文', '').replace(u'努努书坊 版权所有', '')

    # open new text file to fill with novel text
    with open("%s.txt" % title, 'ab') as f:
        f.write(clean_text.encode('utf-8'))
