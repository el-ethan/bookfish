import random
import re
# TODO: document code, change to class

codecs = ['ascii', 'big5', 'big5hkscs', 'cp037', 'cp424', 'cp437', 'cp500', 'cp737', 'cp775', 'cp850', 'cp852', 'cp855', 'cp856', 'cp857', 'cp860', 'cp861', 'cp862', 'cp863', 'cp864', 'cp865', 'cp866', 'cp869', 'cp874', 'cp875', 'cp932', 'cp949', 'cp950', 'cp1006', 'cp1026', 'cp1140', 'cp1250', 'cp1251', 'cp1252', 'cp1253', 'cp1254', 'cp1255', 'cp1256', 'cp1257', 'cp1258', 'euc_jp', 'euc_jis_2004', 'euc_jisx0213', 'euc_kr', 'gb2312', 'gbk', 'gb18030', 'hz', 'iso2022_jp', 'iso2022_jp_1', 'iso2022_jp_2', 'iso2022_jp_2004', 'iso2022_jp_3', 'iso2022_jp_ext', 'iso2022_kr', 'latin_1', 'iso8859_2', 'iso8859_3', 'iso8859_4', 'iso8859_5', 'iso8859_6', 'iso8859_7', 'iso8859_8', 'iso8859_9', 'iso8859_10', 'iso8859_13', 'iso8859_14', 'iso8859_15', 'johab', 'koi8_r', 'koi8_u', 'mac_cyrillic', 'mac_greek', 'mac_iceland', 'mac_latin2', 'mac_roman', 'mac_turkish', 'ptcp154', 'shift_jis', 'shift_jis_2004', 'shift_jisx0213', 'utf_16', 'utf_16_be', 'utf_16_le', 'utf_7', 'utf_8'
    ]

cjk_codecs = [ 'big5', 'big5hkscs', 'cp932', 'cp949', 'cp950', 'euc_jp', 'euc_jis_2004', 'euc_jisx0213', 'euc_kr', 'gb2312', 'gbk', 'gb18030', 'hz', 'iso2022_jp', 'iso2022_jp_1', 'iso2022_jp_2', 'iso2022_jp_2004', 'iso2022_jp_3', 'iso2022_jp_ext', 'iso2022_kr', 'johab', 'shift_jis', 'shift_jis_2004', 'shift_jisx0213', 'utf_16', 'utf_16_be', 'utf_16_le', 'utf_7', 'utf_8'
    ]

zw_codecs = ['gb18030', 'gb2312', 'gbk', 'big5']

class DecoderRing():

    codecs = ['ascii', 'big5', 'big5hkscs', 'cp037', 'cp424', 'cp437', 'cp500', 'cp737', 'cp775', 'cp850', 'cp852', 'cp855', 'cp856', 'cp857', 'cp860', 'cp861', 'cp862', 'cp863', 'cp864', 'cp865', 'cp866', 'cp869', 'cp874', 'cp875', 'cp932', 'cp949', 'cp950', 'cp1006', 'cp1026', 'cp1140', 'cp1250', 'cp1251', 'cp1252', 'cp1253', 'cp1254', 'cp1255', 'cp1256', 'cp1257', 'cp1258', 'euc_jp', 'euc_jis_2004', 'euc_jisx0213', 'euc_kr', 'gb2312', 'gbk', 'gb18030', 'hz', 'iso2022_jp', 'iso2022_jp_1', 'iso2022_jp_2', 'iso2022_jp_2004', 'iso2022_jp_3', 'iso2022_jp_ext', 'iso2022_kr', 'latin_1', 'iso8859_2', 'iso8859_3', 'iso8859_4', 'iso8859_5', 'iso8859_6', 'iso8859_7', 'iso8859_8', 'iso8859_9', 'iso8859_10', 'iso8859_13', 'iso8859_14', 'iso8859_15', 'johab', 'koi8_r', 'koi8_u', 'mac_cyrillic', 'mac_greek', 'mac_iceland', 'mac_latin2', 'mac_roman', 'mac_turkish', 'ptcp154', 'shift_jis', 'shift_jis_2004', 'shift_jisx0213', 'utf_16', 'utf_16_be', 'utf_16_le', 'utf_7', 'utf_8'
    ]

    def __init__(self, mojibake, threshold=1):
        self.mojibake = mojibake
        self.threshold = threshold
        self.moji = self.debake()

    def debake(self):
        # Open file with 2000 most common Chinese characters
        with open('most_common.txt', 'r') as f:
            most_common = f.read()
        all_decoded = {}
        for encoder in codecs:
            try:
                text = bytes(self.mojibake, encoding=encoder)
            except UnicodeEncodeError:
                continue
            for decoder in codecs:
                try:
                    decoded_text = text.decode(decoder)
                except UnicodeDecodeError:
                    continue
                # Save all decoded text to dict
                all_decoded[(encoder, decoder)] = decoded_text

        matches = {}
        for k, v in all_decoded.items():
            # Check for overlap bw decoded string and 2000 most common char
            self.overlap = set(most_common) & set(v)
            if type(self.threshold) == int:
                if (len(self.overlap) >= self.threshold and
                v not in matches.values()):
                    matches[k] = v
            elif type(self.threshold) == float:
                if (len(self.overlap) >= len(set(v)) * self.threshold and
                v not in matches.values()):
                    matches[k] = v
        return matches


    def get_preview(self):
        possible_matches = self.debake()
        for k, v in possible_matches.items():
            print(k, v[:100])   #100 character preview
            selection = input("Does this look right?\n"
                              "Enter 'y' for 'yes', "
                              "or press enter to continue...")
            if not selection:
                continue
            else:
                return k, v
        else:
            print("Sorry, we were unable to decode your mojibake...")
            return None


if __name__ == '__main__':

    with open('mojibake.txt', 'r') as f:
        mojibake = f.read()
    print(decoder_ring(mojibake))

