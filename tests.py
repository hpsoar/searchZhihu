"""Tests for the project."""

import unittest
import urllib.error

from crawl import decode_url, extract_title, extract_link, link_to_url, crawl
from segment import segment
from rank import rank_page


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


class TestLinkToURL(unittest.TestCase):
    """Test link_to_url() in crawl.py."""

    def test_link_to_url(self):
        origin_url = 'http://www.zhihu.com/topic/19554298'
        true_url = 'http://www.zhihu.com/question/21747929'
        link = '/question/21747929'
        url = link_to_url(link, origin_url)
        self.assertEqual(url, true_url)
        link = 'question/21747929'
        url = link_to_url(link, origin_url)
        self.assertEqual(url, true_url)


class TestCrawl(unittest.TestCase):
    """Test crawl() in crawl.py."""

    def test_crawl(self):
        """This test needs temporary database."""
        pass

class TestSegment(unittest.TestCase):
    """Test segment() in segment.py."""

    def test_segment(self):
        string = '写代码是一种怎样的体验？'
        words = segment(string)
        self.assertTrue('写' in words)
        self.assertTrue('代码' in words)
        self.assertTrue('是' not in words)
        self.assertTrue('一种' in words)
        self.assertTrue('怎样' not in words)
        self.assertTrue('体验' in words)

class TestRankPage(unittest.TestCase):
    """Test rank_page() in rank.py."""

    def test_rank_page(self):
        hot_page = decode_url('http://www.zhihu.com/question/28676107')
        cold_page = decode_url('http://www.zhihu.com/question/19555512')
        self.assertTrue(rank_page(hot_page) > rank_page(cold_page))