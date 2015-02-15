"""Various tests of bookfish."""

from urllib.request import urlopen
import unittest
import bookfish
import mjbk



class TestFish(unittest.TestCase):

    def test_made_novel(self):
        test_url = 'http://www.kanunu8.com/book3/7192/'
        f = open('nunu_test.txt', 'r')
        text = f.read()
        f.close()
        self.assertEqual(bookfish.bookfish(test_url), text,
                         "Output does not match test novel")

class TestDecoderRing(unittest.TestCase):

    def test_bake_to_moji(self):
        """Verify that mojibake is correctly converted to characters"""
        mjbk = '¸æËßÎÒ'
        mj = '告诉我'
        moji = mjbk.decoder_ring(mjbk)
        self.assertIn(mj, moji)

if __name__ == "__main__":
    unittest.main()