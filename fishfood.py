# TODO: Write docstrings
import re
from urllib.request import urlopen

def get_text(html, site=None):
    """Extract text from html"""
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

    text = re.sub(junk, '', html)

    # Remove site specific junk from text
    if site == 'nunu':
        for junk in site_junk['nunu']:
            text = text.replace(junk, '')
    # Remove extra whitespace
    text = re.sub(extra_lines, '\n\n', text)
    return text

# Return html from url, if codec is specified,
# html will be decoded using that codec
def get_html(url, codec='gb18030'):
    """Retrieve html from url and decode with codec"""
    response = urlopen(url)
    html = response.read()
    if codec:
        html = str(html.decode(codec))
    return html

def get_chapters(html):
    """Return list of chapter codes from html"""
    re_find_chapters = re.compile('\d{6,}(?=.ht)')
    chapter_codes = re_find_chapters.findall(html)
    return chapter_codes

def get_title(html):
    """Return title of novel"""
    # TODO: get rid of extra stuff in title
    re_find_title = re.search('(?<=<title>).*(?=</title>)', html)
    title = re_find_title.group()
    return title

def get_novel_html(url, codec='gb18030'):
    """Return html of entire novel"""
    html = urlopen(url).read().decode(codec)

    # Find chapter codes
    re_find_chapters = re.compile('\d{6,}(?=.ht)')
    chapter_codes = re_find_chapters.findall(html)
    # Find novel title
    re_find_title = re.search('(?<=<title>).*(?=</title>)', html)
    title = re_find_title.group()

    # Make new urls from chapter codes and compile novel
    html_novel = ''
    for code in chapter_codes:
        new_url = url + code + ".html"
        html = urlopen(new_url).read().decode(codec)
        # Get text from html mess
        html_novel += html
    return html_novel

def bookfish(url, site='nunu', print_to_file=False):
    """Returns full text of novel

    If print_to_file is set to true, a text file
    with the contents of the novel will be created
    as 'title of novel.txt'
    """
    contents_html = get_html(url)
    title = get_title(contents_html)
    html_novel = get_novel_html(url)
    text = get_text(html_novel, site)
    if print_to_file:
        # open new text file to fill with novel text
        with open("%s.txt" % title, 'ab') as f:
            f.write(text.encode('utf-8'))
    else:
        return text


if __name__ == "__main__":
    url = input("Enter a URL:")
    if not url:
        url = 'http://www.kanunu8.com/book3/7192/'
    print(bookfish(url))

