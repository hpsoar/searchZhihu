The default search engine of Zhihu gives poor results, this project tries to
improve searching on Zhihu using page rank and inverted indices.

Here page rank means rank the pages, not Google's PageRank.

The formula used to rank pages on Zhihu is:<pre>
    page_score = answer_count + weight(vote1) + weight(vote2) + weight(vote3)
    Here vote1 to vote3 are the top three answers of the page.</pre>

The formula used to weight votes is:<pre>
    weighted_score = sum((min(vote, range_end) - range_start) * factor
                         for range_start, range_end, factor in ranges)<pre>

The ranges and factors used above are as follows:<pre>
    range          factor        fast_calculate_num
     <= 10           1                 0
     (10, 20]        1/2               5
     (20, 50]        1/4               10
     (50, 500]       1/10              17.5
     (500, 5000]     1/50              57.5
     (5000, inf)     1/100             107.5</pre>

Search results are given by search scores, the search score for a certain page
corresponding to a certain query is:<pre>
    search_score = min(keywords_num, 1) * page_score + extra_score * (keywords_num - 1)
    Here keywords_num is the number of query keywords the pages contains.<pre>

Special thanks to <a href="https://github.com/fxsjy/jieba">jieba</a> project.

MIT license.