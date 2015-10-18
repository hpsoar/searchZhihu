"""Segment queries and pages into keywords."""

import jieba

# Initialize jieba module since jieba use lazy loading
jieba.initialize()

# Build stop words set
with open('stop_words.txt') as file:
    stop_words = {line.replace('\n', '') for line in file.readlines()}


def segment(string):
    """Segment the given string, return keywords list."""
    # The default segmentation allow duplicate words
    words = list(set(jieba.cut_for_search(string)))
    keywords = []
    for word in words:
        if word not in stop_words:
            keywords.append(word.lower())
    return keywords
