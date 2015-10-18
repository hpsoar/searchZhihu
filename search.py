"""Search contents on zhihu.com."""

import string

from segment import segment


def search():
    """Read query from command line, return first 10 search results."""
    pass


digits_and_letters = string.digits + string.ascii_lowercase


def process_query(query):
    """Return (at most) five most distinct keywords in the query."""
    keywords = []
    for words in query:
        keywords += segment(words)
    main_keywords = []
    # Digits and English words are distinctive in Zhihu search
    for keyword in keywords[:]:
        if keyword[0] in digits_and_letters:
            main_keywords.append(keyword)
            keywords.remove(keyword)
    # Sort keywords by length
    keywords.sort(key=len, reverse=True)
    main_keywords.sort(key=len, reverse=True)
    # Extract at most five keywords with descending importance
    main_keywords += keywords[:5]
    return main_keywords[:5]


def get_page_ids(keywords):
    """Return 10 most relevant and important pages by merging and sorting
    pages match each keyword."""
    pass


def get_return_contents(page_ids):
    """Get digests of pages in page_ids."""
    pass


if __name__ == '__main__':
    search()

