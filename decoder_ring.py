def decoder_ring(text, codec=None):
    """decode text and return string"""

    codecs = [
                'utf_8','gb18030', 'gbk',           # Unified
                'gb2312', 'hz', 'iso2022_jp_2',     # Simplified
                'big5hkscs', 'big5', 'cp950',       # Traditional


    ]

    for codec in codecs:

        try:
            text = bytes(text, encoding='utf_8').decode(codec)
        except UnicodeDecodeError:
            print("Codec (%s) failed. Trying next codec..." % codec)
        else:
            print("\"%s\" decoded from %s" % (text, codec))



if __name__ == "__main__":
    text = '¿¡ÇÇÅæ ÇÁ·ÎÁ§Æ®'
    print(decoder_ring(text))