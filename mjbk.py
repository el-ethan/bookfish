import random
import re

codecs = ['ascii', 'big5', 'big5hkscs', 'cp037', 'cp424', 'cp437', 'cp500', 'cp737', 'cp775', 'cp850', 'cp852', 'cp855', 'cp856', 'cp857', 'cp860', 'cp861', 'cp862', 'cp863', 'cp864', 'cp865', 'cp866', 'cp869', 'cp874', 'cp875', 'cp932', 'cp949', 'cp950', 'cp1006', 'cp1026', 'cp1140', 'cp1250', 'cp1251', 'cp1252', 'cp1253', 'cp1254', 'cp1255', 'cp1256', 'cp1257', 'cp1258', 'euc_jp', 'euc_jis_2004', 'euc_jisx0213', 'euc_kr', 'gb2312', 'gbk', 'gb18030', 'hz', 'iso2022_jp', 'iso2022_jp_1', 'iso2022_jp_2', 'iso2022_jp_2004', 'iso2022_jp_3', 'iso2022_jp_ext', 'iso2022_kr', 'latin_1', 'iso8859_2', 'iso8859_3', 'iso8859_4', 'iso8859_5', 'iso8859_6', 'iso8859_7', 'iso8859_8', 'iso8859_9', 'iso8859_10', 'iso8859_13', 'iso8859_14', 'iso8859_15', 'johab', 'koi8_r', 'koi8_u', 'mac_cyrillic', 'mac_greek', 'mac_iceland', 'mac_latin2', 'mac_roman', 'mac_turkish', 'ptcp154', 'shift_jis', 'shift_jis_2004', 'shift_jisx0213', 'utf_16', 'utf_16_be', 'utf_16_le', 'utf_7', 'utf_8'
    ]

cjk_codecs = [ 'big5', 'big5hkscs', 'cp932', 'cp949', 'cp950', 'euc_jp', 'euc_jis_2004', 'euc_jisx0213', 'euc_kr', 'gb2312', 'gbk', 'gb18030', 'hz', 'iso2022_jp', 'iso2022_jp_1', 'iso2022_jp_2', 'iso2022_jp_2004', 'iso2022_jp_3', 'iso2022_jp_ext', 'iso2022_kr', 'johab', 'shift_jis', 'shift_jis_2004', 'shift_jisx0213', 'utf_16', 'utf_16_be', 'utf_16_le', 'utf_7', 'utf_8'
    ]

zw_codecs = ['gb18030', 'gb2312', 'gbk', 'big5']

def decoder_ring(mojibake,
                 encoders=codecs,
                 decoders=codecs):

    moji = {}
    moji_list = []
    for encoder in encoders:
        try:
            mj = bytes(mojibake, encoding=encoder)
        except UnicodeEncodeError:
            continue
        for decoder in decoders:
            try:
                d_moji = mj.decode(decoder)
            except UnicodeDecodeError:
                continue
            if (d_moji not in moji.values()):
                    moji[(encoder, decoder)] = d_moji
                    moji_list.append(d_moji)

    results = {}
    with open('most_common.txt', 'r') as f:
        most_common = f.read()
    for k, v in moji.items():
        overlap = set(most_common) & set(v)
        if len(overlap) >= len(set(v)) * .5:
            results[k] = v

    preview = ''
    for codecs, result in results.items():
        # print(codecs)
        preview += result[:100] + '...End Preview...'

    return preview

if __name__ == '__main__':

    with open('mojibake.txt', 'r') as f:
        mojibake = f.read()
    print(decoder_ring(mojibake))

