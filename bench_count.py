import timeit


# word_list_expr = r'[x for x in re.split("\W", open("moby-dic.txt").read().lower()) if x != ""]'
# 
# print timeit.timeit("count_words.word_count_1(word_list)", setup="import re, count_words;word_list = %s" % word_list_expr, number=10)
# print timeit.timeit("count_words.word_count_2(word_list)", setup="import re, count_words;word_list = %s" % word_list_expr, number=10)
# print timeit.timeit("count_words.word_count_3(word_list)", setup="import re, count_words;word_list = %s" % word_list_expr, number=10)
# print timeit.timeit("count_words.word_count_4(word_list)", setup="import re, count_words;word_list = %s" % word_list_expr, number=10)

# file_name, no = ('moby-dic.txt', 100)
file_name, no = 'large_file.txt', 1

print timeit.timeit("mcw.pool_count('%s')" % file_name, setup="import pool_count_words as mcw",
                    number=no)

print timeit.timeit("mcw.pipe_count('%s')" % file_name, setup="import pipe_count_words as mcw",
                    number=no)

# print timeit.timeit("cw.lazy_count('%s')" % file_name, setup="import count_words as cw",
#                     number=no)
