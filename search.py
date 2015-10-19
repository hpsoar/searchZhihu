"""Search contents on zhihu.com.

Search results are given by search scores, the search score for a certain page
corresponding to a certain query is:
    search_score = min(keywords_num, 1) * page_score +
                       extra_score * (keywords_num - 1)
    Here keywords_num is the number of query keywords the pages contains.
"""

import MySQLdb
import string
import sys

from segment import segment


def search():
    """Read query from command line, return first 10 search results."""
    se_obj = Search(sys.argv[1:])
    se_obj.get_contents()
    return se_obj


digits_and_letters = string.digits + string.ascii_lowercase


class Search:
    """Search class used to build search object."""

    def __init__(self, query):
        # Start index for get_contents()
        self.start = 0
        # Extra_score is awarded to pages contain multiple keywords
        self.extra_score = 200
        self.query = query
        self.keywords = self.process_query()
        self.page_ids = self.get_page_ids()

    def __repr__(self):
        return repr(self.query)

    def process_query(self):

        """Return (at most) five most distinct keywords in the query."""
        keywords = []
        for words in self.query:
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

    def get_page_ids(self):
        """Return 1000 most relevant and important pages by merging and sorting
        pages match each keyword."""
        db = MySQLdb.connect(
            host="localhost", user="coderbai", passwd="dontuseadmin",
            db="zhihu", port=3306, charset="utf8"
        )
        c = db.cursor()
        pages = {}
        # Since the keywords are in descending importance order, fetch pages
        # for keywords in descending number order
        fetch_num = 2000
        step = 250
        # Reduce object reference
        extra_score = self.extra_score
        for keyword in self.keywords:
            c.execute(
                'select page_id, score from keywords where keyword=%s '
                'and score > 0 order by score desc limit %s',
                (keyword, fetch_num)
            )
            for page_id, score in c.fetchall():
                if page_id in pages:
                    pages[page_id] += score + extra_score
                else:
                    pages[page_id] = score
            fetch_num -= step
        c.close()
        db.close()
        sorted_pages = sorted(pages.items(), key=lambda x: x[1], reverse=True)
        return [page[0] for page in sorted_pages[:1000]]

    def get_contents(self):
        """Get digests of pages in page_ids."""
        db = MySQLdb.connect(
            host="localhost", user="coderbai", passwd="dontuseadmin",
            db="zhihu", port=3306, charset="utf8"
        )
        c = db.cursor()
        results = []
        start = self.start
        self.start += 10
        for page_id in self.page_ids[start: start + 10]:
            c.execute('select title, url from pages where page_id=%s',
                      (page_id,))
            results.append(c.fetchone())
        c.close()
        db.close()
        for result in results:
            print(result)
        return results


if __name__ == '__main__':
    search()
