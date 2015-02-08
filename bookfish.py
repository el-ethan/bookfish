# TODO: Write docstrings
import re
from urllib.request import urlopen

def bookfish(url, site='nunu', codec='gb18030', print_to_file=False):
    """Returns full text of novel

    If print_to_file is set to true, a text file
    with the contents of the novel will be created
    as 'title of novel.txt'
    """
    # Get url tail
    # Get html
    html = urlopen(url).read().decode(codec)
    # Get chapters
    re_find_chapters = re.compile('\d{6,}(?=.ht)')
    chapter_codes = re_find_chapters.findall(html)
    # Get title
    re_find_title = re.search('(?<=<title>).*(?=</title>)', html)
    title = re_find_title.group()
    # Get html of novel
    url_tails = {'nunu': '.html',
                 'ifeng': '.htm'
    }
    html_novel = ''
    for code in chapter_codes:
        url_base = re.sub('\.htm$|\.html$', '', url)
        if site == 'ifeng':
            url_base += '/'
        new_url = url_base + code + url_tails[site]
        html = urlopen(new_url).read().decode(codec)
        html_novel += '#'*20 + html

    junk = re.compile('<a.*?</a>'         # Links and associated text
                      '|<.*?>'            # HTML tags
                      '|<!--.*-->'        # HTML comments
                      '|&.*?;',           # Named character references
                      flags=re.DOTALL)
    # Site specific junk to remove
    site_junk = {
            'nunu': ['--正文', '努努书坊 版权所有','|'],
            'yq888': []
    }
    # Extra newlines (2 or more consecutive)
    extra_lines = re.compile('\s{2,}')
    text = re.sub(junk, '', html_novel)

    # Remove site specific junk from text
    if site == 'nunu':
        for junk in site_junk['nunu']:
            text = text.replace(junk, '')
    # Remove extra whitespace
    text = re.sub(extra_lines, '\n\n', text)

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

