"""
bookfish is a scraper that takes the url of the index page of
a Chinese novel as its input, and outputs a text file with the complete
text of the novel.

Currently the url should be from 努努书坊.
"""
# TODO: update docstring
import re
from urllib.request import urlopen
import fishfood


# Return html from url, if codec is specified,
# html will be decoded using that codec
def html_fish(url, codec=None):
    response = urlopen(url)
    html = response.read()
    if codec:
        html = str(html.decode(codec))
    return html

# Take html of table of contents page
# and return (chapter_codes, title) tuple
def chitle_fish(html):
    # Find chapter codes
    re_find_chapters = re.compile('(?<=><a href=")\d+(?=\.)')
    chapter_codes = re_find_chapters.findall(html)
    # Find novel title
    re_find_title = re.search('(?<=<title>).*(?=</title>)', html)
    title = re_find_title.group()
    return chapter_codes, title

# Take a url (of table of contents page) along with
# chapter codes, make new urls, get text from those urls
def bookfish(base_url, chapter_codes,):
    text = ''
    for code in chapter_codes:
        url = base_url + code + ".html"
        html = html_fish(url, codec='gb18030')
    # Remove extraneous text that get_text below doesn't remove
    text += fishfood.clean_food(html, site='nunu')
    return text


if __name__ == '__main__':
    url = input("Please enter a URL:").replace("index.html", "")
    if not url:
        url = 'http://www.kanunu8.com/book3/7192/'

    chapter_codes, title = chitle_fish(html_fish(url, codec='gb18030'))
    print(title)
    print(bookfish(url, chapter_codes))
    # open new text file to fill with novel text
    # with open("%s.txt" % title, 'ab') as f:
    #     f.write(text.encode('utf-8'))




