"""Various tests of bookfish."""
import unittest
import bookfish
from urllib.request import urlopen


class TestFish(unittest.TestCase):

    def test_made_novel(self):
        test_url = 'http://www.kanunu8.com/book3/7192/'
        f = open('xiaoshuo.txt', 'r')
        text = f.read()
        f.close()
        self.assertEqual(bookfish.bookfish(test_url), text,
                         "Output does not match test novel")

if __name__ == "__main__":
    unittest.main()