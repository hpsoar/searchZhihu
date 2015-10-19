The default search engine of Zhihu gives poor results, this project tries to
improve searching on Zhihu using page rank and inverted indices.

Here page rank means rank the pages, not Google's PageRank.

The formula used to rank pages on Zhihu is:<pre>
    page_score = answer_count + weight(vote1) + weight(vote2) + weight(vote3)
    Here vote1 to vote3 are the top three answers of the page.</pre>

The formula used to weight votes is:<pre>
    weighted_score = sum((min(vote, range_end) - range_start) * factor
                         for range_start, range_end, factor in ranges)</pre>

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
    Here keywords_num is the number of query keywords the pages contains.</pre>

Example:
$ python3 search.py 怎样学习编程？

> ('我学编程为什么难？是思维方式不对还是学习方式不对？', 'http://www.zhihu.com/question/27436363')
> ('26 岁开始学编程晚了吗？', 'http://www.zhihu.com/question/19562626')
> ('初中生学习编程是不务正业吗？', 'http://www.zhihu.com/question/24693675')
> ('你会如何重新学习编程？', 'http://www.zhihu.com/question/31862619')
> ('30 岁才开始学习编程靠谱吗？', 'http://www.zhihu.com/question/20796653')
> ('编程零基础应当如何开始学习 Python ？', 'http://www.zhihu.com/question/20039623')
> ('15 岁高一少年自学学习会了 iOS 和 C++ 编程，这说明此人是个天才么？', 'http://www.zhihu.com/question/27382334')
> ('那些初高中甚至小学就接触编程的人最后到了什么样的境界？', 'http://www.zhihu.com/question/28159715')
> ('学习编程用什么做笔记比较好？', 'http://www.zhihu.com/question/21438053')
> ('对于一个编程基础不是很好的学生来说，学习数据挖掘、机器学习之类的并以后从事这样的工作靠谱吗？', 'http://www.zhihu.com/question/28523857')

Special thanks to <a href="https://github.com/fxsjy/jieba">jieba</a> project.

MIT license.