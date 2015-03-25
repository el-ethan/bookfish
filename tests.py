"""Various tests of bookfish module"""

import unittest
import bookfish

class TestFish(unittest.TestCase):

    def test_made_novel(self):
        test_url = 'http://www.kanunu8.com/book3/7192/'
        with open('nunu_test.txt', 'r') as f:
            expected_book = f.read()
        bf = bookfish.Bookfish(test_url)
        observed_book = bf.book
        title = bf.title
        site = bf.site_name
        self.assertEqual(bf.url, test_url)
        self.assertEqual(title, "古典爱情 - 余华 - 小说在线阅读 - 努努书坊")
        self.assertEqual(site, "nunu")
        self.assertEqual(observed_book, expected_book,
                         "Output does not match test novel")





if __name__ == "__main__":
    unittest.main()