import multiprocessing as mp
import sys
import itertools
import re
import collections

CPU_COUNT = mp.cpu_count()

def chunk_format(chunk):
    return [word for word in re.split("\W", chunk.lower()) if word != '']


def count_chunk(chunk):
    def _increment_key(d, word):
        d[word] += 1 
        return d

    return reduce(_increment_key, chunk_format(chunk), collections.defaultdict(int))

def file_chunker(file_name, chunk_size):
    prev = ''
    with open(file_name, 'r') as f:
        new = f.read(chunk_size)
        while new:
            yield prev + new[:new.rfind(' ')]
            prev = new[new.rfind(' '):]
            new = f.read(chunk_size)


def _combine_counts(d1, d2):
    for (word, count) in d2.iteritems():
        d1[word] += count

    return d1


def combine_counts(word_counts):
    return reduce(_combine_counts, word_counts, collections.defaultdict(int))


def pool_count(file_name, most_common=10):
    pool = mp.Pool(processes=CPU_COUNT)

    word_counts = pool.map(count_chunk, file_chunker(file_name, 2 ** 19))

    return sorted(combine_counts(word_counts).iteritems(),
                  key=lambda x: x[1], reverse=True)[:most_common]


def profile(fn, file_name="large_file.txt"):
    fn(file_name)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "profile":
        import cProfile
        cProfile.run("profile(%s)" % sys.argv[2])

    else:
        print pool_count("moby-dic.txt")
