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

# Header used to open urls.
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
              'image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
}


def decode_url(url):
    """Decode html file from url to string."""
    try:
        response = open_url(url, HEADERS)
    except:
        raise
    compressed = response.getheader('Content-Encoding')
    # limit the bytes read from response in case decode non-text file
    if compressed:
        compressed_file = response.read(524288)
        file_bytes = gzip.decompress(compressed_file)
    else:
        file_bytes = response.read(1048576)
    charset = response.info().get_content_charset()
    if charset:
        file_string = file_bytes.decode(charset)
    else:
        try:
            charset = 'utf-8'
            file_string = file_bytes.decode(charset)
        except UnicodeDecodeError:
            charset = 'gb18030'
            file_string = file_bytes.decode(charset)
    # Close response object
    response.close()
    return file_string


def open_url(url, headers):
    """Open url using urllib library, return the response."""
    request = urllib.request.Request(url, headers=headers)
    try:
        response = urllib.request.urlopen(request, timeout=5)
    except urllib.error.URLError:
        raise
    else:
        return response
link_pattern = re.compile(
    r'href=["\'](?P<link>/question/\d+)["\']'
)

def extract_link(html):
    """Extract web page links from html string. Here we only extract
    question links."""
    return re.findall(link_pattern, html)


title_pattern = re.compile(
    r'<title>(?P<title>[^<]+)</title>'
)


def extract_title(html):
    """Extract title of a web page.

    Only the main title is extracted.
    For example, given <title>什么才算是真正的编程能力？ - 计算机科学 - 知乎</title>,
    return 什么才算是真正的编程能力？.
    """
    match = title_pattern.search(html[:5000])
    title = match.group('title').strip()
    main_title = title.split(' ', maxsplit=1)[0]
    return main_title


def log_error(error):
    """Log errors during crawl."""
    pass
