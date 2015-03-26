#!/usr/bin/env python3
"""Various tests of bookfish module"""

import unittest
import bookfish

# Link to index page of 古典爱情 by 余华
test_url = 'http://www.kanunu8.com/book3/7192/'

class TestFish(unittest.TestCase):

    def test_find_chapter_urls(self):
        """Verify that the right amount of chapters are found"""
        chapters = bookfish.find_chapter_urls(test_url)
        self.assertEqual(len(chapters), 6)

    def test_no_tags(self):
        """Verify that all HTML tags have been removed from text"""
        pass


if __name__ == "__main__":
    unittest.main()