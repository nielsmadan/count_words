import multiprocessing
import collections
import sys
import re
import operator

# idiomatic, using collection Counter type
def word_count_1(wl, most_common=10):
    return collections.Counter(wl).most_common(most_common)


# pretending Counter object does not exist, slightly faster than word_count_1
def word_count_2(wl, most_common=10):
    def _increment_key(d, word):
        d[word] += 1 
        return d

    return sorted(reduce(_increment_key, wl, collections.defaultdict(int)).iteritems(), key=lambda x: x[1], reverse=True)[:most_common]


# create a new list of every 100th word in the text, find the 20 most common words in that new list.
# discard all the other words in the text, and run the complete word count on the remainder.
# about twice as fast as word_count_2
def word_count_3(word_list, step=10, num_seed=20):
    most_common_set = set([word for word, num in word_count_2(word_list[::step], num_seed)])

    return word_count_2([word for word in word_list if word in most_common_set])


# get the word count of every 10th word in the text, extrapolate towards the total word count
# about twice as fast as word_count_3 with average error of 2.8%.
def word_count_4(word_list, step=10):
    most_common = word_count_2(word_list[::step])

    return [(w, n * step) for (w, n) in most_common]


# calculate the difference in word count between real result and approximation
def calc_diff(word_list, step=10):
    real_result = word_count_2(word_list)
    approx_result = dict(word_count_4(word_list, step))

    def percentage(a, b):
        return abs(100 * a / float(b) - 100)

    return [(word, percentage(result, approx_result[word])) for word, result in real_result]


def line_format(line):
    return [word for word in re.split("\W", line.lower()) if word != '']


def lazy_line_reader(file_name, fmt):
    return (word for line in open(file_name)
                 for word in fmt(line))


def lazy_count(file_name, most_common=10):
    def _increment_key(d, word):
        d[word] += 1 
        return d

    return sorted(reduce(_increment_key, lazy_line_reader(file_name, line_format), collections.defaultdict(int)).iteritems(), key=lambda x: x[1], reverse=True)[:most_common]


def profile(fn, words=[x for x in re.split("\W", open("moby-dic.txt").read().lower()) if x != '']):
    fn(words)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "profile":
        import cProfile
        cProfile.run("profile(%s)" % sys.argv[2])

    elif len(sys.argv) > 1 and sys.argv[1] == "large":
        print lazy_count("large_file.txt")

    else:
        word_list = [x for x in re.split("\W", open("moby-dic.txt").read().lower()) if x != '']

        print word_count_1(word_list)
        print word_count_2(word_list)
        print word_count_3(word_list)
        print word_count_4(word_list)
        print lazy_count("moby-dic.txt")
        print ["%s: %.2f" % (word, res) for word, res in calc_diff(word_list)]
        print "%.2f" % (reduce(operator.add, [res for word, res in calc_diff(word_list)]) / 10)
