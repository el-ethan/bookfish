import re
# TODO: Write docstring
def clean_food(html, site=None):
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

if __name__ == "__main__":

    sample_html = """

    <html>
    <head>
    <title> Chapter 1 - 杀手，回光返照的命运 - 小说在线阅读 - 九把刀</title>
    <meta http-equiv="Content-Type" content="text/html; charset=gbk">
    <link href="/templets/style/kanunu6.css" rel="stylesheet" type="text/css" />
    <style type="text/css">
    <!--
    body {
        margin-left: 0px;
        margin-top: 0px;
        margin-right: 0px;
        margin-bottom: 0px;
        background-color: #464646;
    }
    .style1 {color: #FFFFFF}
    -->
    &nbsp;&nbsp;&nbsp;&nbsp;我坐在会议桌上，跟七个老头一起开会，但会议记录上没有半个字，因为他们在一分钟前全死光了。我特别喜欢接这种整个杀光抹净的单——我猜我以前一定是一个非常压抑的人，所以现在见鬼了特别喜欢解放自己。<br />
    <script language="javascript" type="text/javascript" src="/advs/2024/bd01.js"></script>
    <script language="javascript" type="text/javascript" src="/tj.js"></script>
    </body>
    </html>

    """
    print("Sample input:\n", sample_html)
    print("Sample output:\n", clean_food(sample_html, site='nunu'))