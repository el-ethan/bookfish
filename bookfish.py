"""
bookfish is a scraper that takes the url of the index page of
a Chinese novel as its input, and outputs a text file with the complete
text of the novel.

Currently the url should be from 努努书坊.
"""
# TODO: update docstring
import re
from urllib.request import urlopen

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

def chapter_fish(html):
    # Find chapter codes
    re_find_chapters = re.compile('(?<=><a href=")\d+(?=\.)')
    chapter_codes = re_find_chapters.findall(html)
    return chapter_codes

def title_fish(html):
    re_find_title = re.search('(?<=<title>).*(?=</title>)', html)
    title = re_find_title.group()
    return title

def cleaner_fish(html, site=None):
    """docstring"""
    junk = re.compile('<a.*?</a>'         # Links and associated text
                      '|<.*?>'            # HTML tags
                      '|<!--.*-->'        # HTML comments
                      '|&.*?;',           # Named character references
                      flags=re.DOTALL)
    # TODO: Change to regex so I can handle things like: '业务QQ: \d*'
    # Site specific junk to remove
    site_junk = {
            'nunu': ['--正文', '努努书坊 版权所有','|'],
            'yq888': []
    }
    # Extra newlines (2 or more consecutive)
    extra_lines = re.compile('\s{2,}')

    clean_text = re.sub(junk, '', html)

    # Remove site specific junk from text
    if site == 'nunu':
        for junk in site_junk['nunu']:
            clean_text = clean_text.replace(junk, '')
    # Remove extra whitespace
    clean_text = re.sub(extra_lines, '\n\n', clean_text)
    return clean_text

# Take a url (of table of contents page) along with
# chapter codes, make new urls, get text from those urls
def bookfish(base_url, chapter_codes,):
    text = ''
    for code in chapter_codes:
        url = base_url + code + ".html"
        html = html_fish(url, codec='gb18030')
        # Remove extraneous text that get_text below doesn't remove
        text += cleaner_fish(html, site='nunu')
    return text

if __name__ == '__main__':

    url = input("Please enter a URL:").replace("index.html", "")
    if not url:
        url = 'http://www.kanunu8.com/book3/7192/'

    chapter_codes = chapter_fish(html_fish(url, codec='gb18030'))
    print(title_fish(html_fish(url, codec='gb18030')))
    print(bookfish(url, chapter_codes))
    # open new text file to fill with novel text
    # with open("%s.txt" % title, 'ab') as f:
    #     f.write(text.encode('utf-8'))




