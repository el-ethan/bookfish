"""Various tests of bookfish."""
import unittest
import fishfood
import bookfish
from urllib.request import urlopen

test_url = 'http://www.kanunu8.com/book3/7192/'
test_html = urlopen(test_url).read().decode('gb18030')
class TestFood(unittest.TestCase):

    def test_get_title(self):
        self.assertEqual(bookfish.get_title(test_html),
                        '古典爱情 - 余华 - 小说在线阅读 - 努努书坊',
                        "Title doesn't match")
    def test_get_html(self):
        self.assertEqual(bookfish.get_html(test_url),
                        test_html,
                        "HTML doesn't match")

if __name__ == "__main__":
    unittest.main()