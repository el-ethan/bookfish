# TODO: Write docstrings
import re
from urllib.request import urlopen

def bookfish(url, codec='gb18030', print_to_file=False):
    """Returns full text of novel

    If print_to_file is set to true, a text file
    with the contents of the novel will be created
    as 'title of novel.txt'
    """
    sites = ['nunu', 'yanqing888', 'hexun']
    for site_name in sites:
        if site_name in url:
            site = site_name
    # Get url tail
    # Get html
    html = urlopen(url).read().decode(codec)
    # Get title
    re_find_title = re.search('(?<=<title>).*(?=</title>)', html)
    title = re_find_title.group()
    # Get chapters
    if site == 'nunu':
        re_find_tails = re.compile('(?<=<a href=")\d+.html?')
    elif site == 'yanqing888':
        re_find_tails = re.compile('(?<=<a href=")\d+.html')
    elif site == 'hexun':
        re_find_tails = re.compile('(?<=<a href="/)chapter[-\d\w]+.shtml')
    url_tails = re_find_tails.findall(html)
    # Get html of novel
    html_novel = ''
    for tail in url_tails:
        url_base = re.sub('\.html?$|book-\d+.shtml', '', url)
        new_url = url_base + tail
        html = urlopen(new_url).read().decode(codec)
        html_novel += '#'*20 + html

    if site == 'nunu':
        text = re.sub('<a.*?</a>'
                      '|<.*?>'
                      '|<!--(.*\n)+?-->'
                      '|&.*?;', '', html_novel)
    elif site == 'hexun':
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
                      '|..onclick=.*', '', html_novel)
    # Site specific junk to remove
    site_junk = {'nunu': ['--正文', '努努书坊 版权所有','|'
                 ],
                 'hexun': ['if(w_frame.readyState)', 'else', '*/', '/*'
                 ]
    }

    # Extra newlines (2 or more consecutive)
    extra_lines = re.compile('\s{2,}')
    # Remove site specific junk from text
    for junk in site_junk[site]:
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
        url = 'http://data.book.hexun.com/book-19250.shtml'
    print(bookfish(url))

