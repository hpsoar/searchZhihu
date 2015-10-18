"""Rank web pages on zhihu.com.

The formula used to rank pages is:
    page_score = answer_count + weight(vote1) + ... + weight(vote3)
    Here vote1 to vote3 are the top three answers of the page.

The formula used to weight votes is:
    weighted_score = sum((min(vote, range_end) - range_start) * factor
                         for range_start, range_end, factor in ranges)
    range          factor        fast_calculate_num
     <= 10           1                 0
     (10, 20]        1/2               5
     (20, 50]        1/4               10
     (50, 500]       1/10              17.5
     (500, 5000]     1/50              57.5
     (5000, inf)     1/100             107.5
"""

import MySQLdb
import re

from segment import segment

vote_count_pattern = re.compile(
    r'data-votecount="(?P<count>\d+)"'
)
answer_count_pattern = re.compile(
    r'data-num="(?P<count>\d+)"'
)


def rank_page(html):
    """Given an Zhihu html file, return a score indicates its importance."""
    votes = [int(count) for count in re.findall(vote_count_pattern, html)]
    # In case there is only one answer
    answer_count = len(votes)
    answer_count_match = answer_count_pattern.search(html)
    if answer_count_match:
        answer_count = int(answer_count_match.group('count'))
    # Use top five answers to compute page rank
    votes.sort(reverse=True)
    votes = votes[:3]
    score = answer_count
    for vote in votes:
        score += weight_vote(vote)
    return score


factors = {
    10: 0.5,
    20: 0.25,
    50: 0.1,
    500: 0.02,
    5000: 0.01,
}
fast_calculate = {
    10: 5,
    20: 10,
    50: 17.5,
    500: 57.5,
    5000: 107.5,
}


def weight_vote(vote):
    """Compute the weight of a vote. See docstring on the top."""
    if vote > 5000:
        score = vote * factors[5000] + fast_calculate[5000]
    elif vote > 500:
        score = vote * factors[500] + fast_calculate[500]
    elif vote > 50:
        score = vote * factors[50] + fast_calculate[50]
    elif vote > 20:
        score = vote * factors[20] + fast_calculate[20]
    elif vote > 10:
        score = vote * factors[10] + fast_calculate[10]
    else:
        score = vote
    return int(score)
