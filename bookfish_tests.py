#!/usr/bin/env python3
"""Various tests of bookfish module"""

import unittest
from bookfish import Bookfish



# Link to index page of 古典爱情 by 余华
test_url = 'http://www.kanunu8.com/book3/7192/'

# Bookfish object to be tested
fish = Bookfish(test_url)

class TestFish(unittest.TestCase):

    def test_right_number_of_chapters(self):
        """Verify that the right amount of chapters are found"""
        chapters = fish.find_chapter_urls()
        self.assertEqual(len(chapters), 6)

    def test_right_form_of_chapter_urls(self):
        """Verify that chapter urls are of the right form"""
        chapters = fish.chapters
        for chapter_url in chapters:
            self.assertRegex(chapter_url, r'http://www\.kanunu8\.com.*\.html')

    def test_title(self):
        expected_title = '古典爱情'
        title = fish.title
        self.assertEqual(title, expected_title)

    def test_author(self):
        expected_author = '余华'
        author = fish.author
        self.assertEqual(author, expected_author)

    def test_book_length(self):
        pass




    # def test_no_tags(self):
    #     """Verify that all HTML tags have been removed from text"""
    #     raise AssertionError("Tests not yet written")


if __name__ == "__main__":
    unittest.main()