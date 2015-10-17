"""Fetch contents on zhihu.com."""

import MySQLdb
import gzip
import re
import time
import urllib.error
import urllib.request



def crawl(start_url):
    """Crawl zhihu.com and store pages to local database."""
    pass


def decode_url(url):
    """Decode html file from url to string."""
    pass


def open_url(url):
    """Open url using urllib library, return the response."""
    pass


def extract_link(html):
    """Extract web page links from html string."""
    pass


def extract_title(html):
    """Extract title of a web page."""
    pass


def log_error(error):
    """Log errors during crawl."""
    pass
