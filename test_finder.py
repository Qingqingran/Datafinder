"""Unit test for Finder."""

import unittest
from finder import Finder


class TestFinder(unittest.TestCase):

    def test_find_email(self):
        text = """This is a email address: evita@ustc.edu.cn, and another: asdf25_453@outlook.com."""
        f = Finder(text)
        result = f.find_email()
        self.assertEqual(
            [
                (25, 42),
                (57, 79)
            ],
            result
        )

    def test_find_phonenum(self):
        text = """My phone: 13345662777. Not 2133456627777."""
        f = Finder(text)
        result = f.find_phonenum()
        self.assertEqual(
            [
                (10, 21)
            ],
            result
        )

    def test_find_all(self):
        pass
