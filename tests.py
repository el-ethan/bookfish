"""Various tests of bookfish."""
import unittest
import fishfood
import bookfish
from urllib.request import urlopen

test_url = 'http://www.kanunu8.com/book3/7192/'
test_html = urlopen(test_url).read()
class TestFood(unittest.TestCase):

    def test_html_fish_with_codec(self):
        self.assertEqual(bookfish.html_fish(test_url, codec='gb18030'),
                        test_html.decode('gb18030'),
                        "Decoded HTML output of function not as expected")

    def test_html_fish_no_codec(self):
        self.assertEqual(bookfish.html_fish(test_url),
                        test_html,
                        "HTML output of function not as expected")

if __name__ == "__main__":
    unittest.main()