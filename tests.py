"""Tests for the project."""

import unittest
import urllib.error

from crawl import decode_url


class TestDecodeURL(unittest.TestCase):
    """Test decode_url() in crawl.py."""

    def test_decode_url(self):
        html = decode_url('http://www.zhihu.com')
        self.assertTrue('知乎' in html[:1000])
        # Unit test with Chinese characteristics
        with self.assertRaises(urllib.error.URLError):
            decode_url('https://www.google.com')
