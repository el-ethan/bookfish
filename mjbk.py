# TODO: document code

class DecoderRing():

    codecs = ['ascii', 'big5', 'big5hkscs', 'cp037', 'cp424', 'cp437', 'cp500', 'cp737', 'cp775', 'cp850', 'cp852', 'cp855', 'cp856', 'cp857', 'cp860', 'cp861', 'cp862', 'cp863', 'cp864', 'cp865', 'cp866', 'cp869', 'cp874', 'cp875', 'cp932', 'cp949', 'cp950', 'cp1006', 'cp1026', 'cp1140', 'cp1250', 'cp1251', 'cp1252', 'cp1253', 'cp1254', 'cp1255', 'cp1256', 'cp1257', 'cp1258', 'euc_jp', 'euc_jis_2004', 'euc_jisx0213', 'euc_kr', 'gb2312', 'gbk', 'gb18030', 'hz', 'iso2022_jp', 'iso2022_jp_1', 'iso2022_jp_2', 'iso2022_jp_2004', 'iso2022_jp_3', 'iso2022_jp_ext', 'iso2022_kr', 'latin_1', 'iso8859_2', 'iso8859_3', 'iso8859_4', 'iso8859_5', 'iso8859_6', 'iso8859_7', 'iso8859_8', 'iso8859_9', 'iso8859_10', 'iso8859_13', 'iso8859_14', 'iso8859_15', 'johab', 'koi8_r', 'koi8_u', 'mac_cyrillic', 'mac_greek', 'mac_iceland', 'mac_latin2', 'mac_roman', 'mac_turkish', 'ptcp154', 'shift_jis', 'shift_jis_2004', 'shift_jisx0213', 'utf_16', 'utf_16_be', 'utf_16_le', 'utf_7', 'utf_8'
    ]

    def __init__(self, mojibake):
        self.mojibake = mojibake
        self.moji = self.debake()[0]
        self.encdec = ("====================\n"
                       "Encoded with: {0}\n"
                       "Decoded with: {1}\n"
                       "====================\n"
                       .format(self.debake()[1],self.debake()[2]))
        self.verbose = self.debake()[3]

    def debake(self):
        # Open file with 2000 most common Chinese characters
        with open('most_common.txt', 'r') as f:
            most_common = f.read()
        all_decoded = {}
        for encoder in self.codecs:
            try:
                text = bytes(self.mojibake, encoding=encoder)
            except UnicodeEncodeError:
                continue
            for decoder in self.codecs:
                try:
                    decoded_text = text.decode(decoder)
                except UnicodeDecodeError:
                    continue
                # Save all decoded text to dict
                all_decoded[(encoder, decoder)] = decoded_text

        max_overlap = 0
        best_fit = {}
        for k, v in all_decoded.items():
            # Overlap of characters in decoded text and 2000 most common ones
            self.overlap = set(most_common) & set(v)
            # Check if overlap is greater than previous overlap
            if len(self.overlap) > max_overlap:
                max_overlap = len(self.overlap)
                best_fit = v
                encoder = k[0]
                decoder = k[1]
        return best_fit, encoder, decoder, all_decoded

if __name__ == '__main__':

    with open('mojibake.txt', 'r') as f:
        mojibake = f.read()
    mojibake = input("Type your mojibake: ")
    print(DecoderRing(mojibake).moji)
    print(DecoderRing(mojibake).encdec)
    print(DecoderRing(mojibake).verbose)


