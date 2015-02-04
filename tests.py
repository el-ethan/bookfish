"""Various tests of bookfish."""
import unittest
import fishfood

class TestFood(unittest.TestCase):

    def test_rm_html_tags(self):
        html = "<title>Chapter 1 - 杀手，回光返照的命运 - 九把刀</title>"
        text = "Chapter 1 - 杀手，回光返照的命运 - 九把刀"
        self.assertEqual(fishfood.clean_food(html), text)

    def test_rm_html_comments(self):
        html_comment = """<!--
                            body {
                                margin-left: 0px;
                                margin-top: 0px;
                                margin-right: 0px;
                                margin-bottom: 0px;
                                background-color: #464646;
                            }
                            .style1 {color: #FFFFFF}
                            -->"""
        self.assertEqual(fishfood.clean_food(html_comment), '')

if __name__ == "__main__":
    unittest.main()