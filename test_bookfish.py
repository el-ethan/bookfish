#!/usr/bin/env python3
"""Various tests of bookfish module"""

import unittest
import os
from bookfish import Bookfish



# Link to index page of 古典爱情 by 余华
test_url = 'http://www.kanunu8.com/book3/7192/'

nunu_urls = [test_url,
             'http://www.kanunu8.com/book/4397/index.html',
             'http://www.kanunu8.com/book3/7385/',
             'http://www.kanunu8.com/book3/8243/',
]
# Bookfish object to be tested
fish = Bookfish(test_url)

class TestFish(unittest.TestCase):

    def test_right_number_of_chapter_urls(self):
        """Verify that the right amount of chapters are found"""
        chapters = fish.find_chapter_urls()
        self.assertEqual(len(chapters), 6)

    def test_right_form_of_chapter_urls(self):
        """Verify that chapter urls are of the right form"""
        chapter_urls = fish.chapters
        for url in chapter_urls:
            self.assertRegex(url, r'http://www\.kanunu8\.com.*\.html')

    def test_title(self):
        "Verify title is as expected"
        expected_title = '古典爱情'
        title = fish.title
        self.assertEqual(title, expected_title)

    def test_author(self):
        """Verify author is as expected"""
        expected_author = '余华'
        author = fish.author
        self.assertEqual(author, expected_author)

    def test_no_html_tags(self):
        """Verify that normal html tags have been removed from text"""
        self.assertNotRegex(fish.book, r'<.*?>')

    def test_no_html_entities(self):
        """Verify no html entities in final text"""
        self.assertNotRegex(fish.book, r'&.*?;')

    def test_right_number_chapters_in_book(self):
        """Verify that the right number of chapters is processed"""
        chap_sep = '*' * 80
        chapter_count = fish.book.count(chap_sep)
        self.assertEqual(chapter_count, 6)

    def test_char_count(self):
        """Verify that text has the expected amount of characters"""
        self.assertEqual(fish.charcount, 23838)

    def test_file_saved(self):
        fish = Bookfish(test_url, print_to_file=True)
        saved_file = '{0}_{1}.txt'.format(fish.title, fish.author)
        self.assertTrue(os.path.exists(saved_file))
        os.remove(saved_file)

class TestGeneral(unittest.TestCase):

    def test_bulk_urls(self):
        """Verify multiple urls pass general tests of length and content"""
        for url in nunu_urls:
            fish = Bookfish(url)
            chapter_urls = fish.find_chapter_urls()
            chap_sep = '*' * 80
            chapter_count = fish.book.count(chap_sep)
            self.assertGreater(chapter_count, 1)
            self.assertGreater(len(chapter_urls), 1)
            self.assertGreater(fish.charcount, 100)
            self.assertNotRegex(fish.book, r'&.*?;')
            self.assertNotRegex(fish.book, r'<.*?>')
            self.assertIsNotNone(fish.author)
            self.assertIsNotNone(fish.title)

if __name__ == "__main__":
    unittest.main()
