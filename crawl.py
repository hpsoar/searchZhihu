"""Fetch contents on zhihu.com."""

import MySQLdb
import gzip
import re
import time
import urllib.error
import urllib.request


def crawl(base_url, start, crawl_num=1000):
    """Crawl zhihu.com and store pages to local database."""
    db = MySQLdb.connect(
        host="localhost", user="coderbai", passwd="dontuseadmin",
        db="zhihu", port=3306, charset="utf8"
    )
    c = db.cursor()
    for page_num in range(start, start + crawl_num):
        page_url = base_url + str(page_num)
        try:
            page_html = decode_url(page_url)
        except urllib.request.HTTPError as error:
            log_error(page_url, error)
            # 404 code indicate page_num exceeds max page number on zhihu.com
            if error.code == 404:
                break
            continue
        except urllib.request.URLError as error:
            log_error(page_url, error)
            continue
        print('Start crawl page' + str(page_num) + '\n')
        question_urls = [link_to_url(link, page_url)
                         for link in extract_link(page_html)]
        for question_url in question_urls:
            time.sleep(0.5)
            try:
                question_html = decode_url(question_url)
            except urllib.request.URLError as error:
                log_error(question_url, error)
                continue
            title = extract_title(question_html)
            question_id = int(question_url.rsplit('/', maxsplit=1)[-1])
            c.execute(
                'insert into pages (page_id, url, title, content) values '
                '(%s, %s, %s, %s) on duplicate key update title=values(title), '
                'content=values(content)',
                (question_id, question_url, title, question_html)
            )
            # Commit transactions, otherwise insertion will fail
            db.commit()
    c.close()
    db.close()
    print('Crawl from page {0} to page {1} finished!'.format(
        str(start), str(start + crawl_num)))

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
    title = match.group('title')
    main_title = title.split('-', maxsplit=1)[0].strip()
    return main_title

# This url pattern was built for production use, not following RFC 3986.
url_pattern = re.compile(
    r'(?P<protocol>https?://)'
    r'(?P<host>([A-Za-z\d][A-Za-z\d\-]{0,61}[A-Za-z\d]?\.)+[A-Za-z\d]{2,7})'
    r'(?P<port>:\d{1,5})?'
    r'(?P<path>/.*)?'
)


def link_to_url(link, origin_url):
    """Convert a link from origin_url to a valid url."""
    url_match = url_pattern.match(origin_url)
    protocol = url_match.group('protocol')
    host = url_match.group('host')
    port = url_match.group('port')
    if port:
        host += port
    if link.startswith('http'):
        url = link
    elif link.startswith('//'):
        url = protocol + link[2:]
    elif link.startswith('/'):
        url = protocol + host + link
    else:
        url = protocol + host + '/' + link
    return url


def log_error(url, error):
    """Log errors during crawl."""
    error_info = ''.join([
        'Fail to decode: ', url, '\n', 'Error reason: ', error.reason, '\n'
    ])
    with open('error_log.txt', 'a') as file:
        file.write(error_info)


if __name__ == '__main__':
    crawl('http://www.zhihu.com/topic/19554298/questions?page=', 1, 5000)
