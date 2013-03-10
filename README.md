counting words in python
========================

This script will count up all the words in a text file in various ways and output the most common ones.

Use get_moby_dic.sh to get the text file. Use make_large_file.sh to duplicate the file 512 times and create a large
text file to appreciate the lazy solution.

This will count up the words in the small file in various ways.

 python count_words.py

This will cProfile the count_words_1 solution (replace function name to profile something else);

 python count_words.py profile count_words_1

This will benchmark solutions against each other:

 python bench_count.py
