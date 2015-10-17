"""Tests for the project."""

import unittest
import urllib.error

from crawl import decode_url, extract_title, extract_link


class TestDecodeURL(unittest.TestCase):
    """Test decode_url() in crawl.py."""

    def test_decode_url(self):
        html = decode_url('http://www.zhihu.com')
        self.assertTrue('知乎' in html[:1000])
        # Unit test with Chinese characteristics
        with self.assertRaises(urllib.error.URLError):
            decode_url('https://www.google.com')


class TestExtractTitle(unittest.TestCase):
    """Test extract_title() in crawl.py."""

    def test_extract_title(self):
        html = decode_url('http://www.zhihu.com')
        title = extract_title(html)
        self.assertEqual(title, '知乎')

class TestExtractLink(unittest.TestCase):
    """Test extract_link() in crawl.py."""

    def test_extract_link(self):
        html = decode_url('http://www.zhihu.com')
        links = extract_link(html)
        self.assertEqual(links, [])
        html = decode_url('http://www.zhihu.com/topic/19554298')
        links = extract_link(html)
        self.assertTrue(len(links) > 5)