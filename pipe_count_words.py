import multiprocessing as mp
import sys
import re
import collections


def chunk_format(chunk):
    return [word for word in re.split("\W", chunk.lower()) if word != '']


def _combine_counts(d1, d2):
    for (word, count) in d2.iteritems():
        d1[word] += count

    return d1


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


def chunk_producer(file_name, chunk_size, pipe):
    out_conn, _ = pipe
    for chunk in file_chunker(file_name, chunk_size):
        out_conn.send(chunk)

    out_conn.close()


def chunk_counter(pipe1, pipe2):
    closep, in_conn = pipe1
    closep.close()
    out_conn, _ = pipe2
    try:
        while True:
            out_conn.send(count_chunk(in_conn.recv()))
    except EOFError:
        out_conn.close()


def count_merger(unused_pipes, in_pipe, out_pipe):
    closep, in_conn = in_pipe
    closep.close()
    out_conn, _ = out_pipe

    for pipe in unused_pipes:
        closep, _ = pipe
        closep.close()

    d = collections.defaultdict(int)
    try:
        while True:
            d = _combine_counts(d, in_conn.recv())
    except EOFError:
        out_conn.send(d)
        out_conn.close()


def pipe_count(file_name, most_common=10):
    pipe1 = mp.Pipe(True)
    p1 = mp.Process(target=chunk_producer, args=(file_name, 2 ** 19, pipe1,))
    p1.start()

    pipe2 = mp.Pipe(True)
    p2 = mp.Process(target=chunk_counter, args=(pipe1, pipe2,))
    p2.start()

    pipe3 = mp.Pipe(True)
    p3 = mp.Process(target=count_merger, args=([pipe1], pipe2, pipe3))
    p3.start()

    pipe1[0].close()
    pipe2[0].close()
    pipe3[0].close()

    return sorted(pipe3[1].recv().iteritems(), key=lambda x: x[1], reverse=True)[:most_common]

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "profile":
        import cProfile
        cProfile.run("profile(%s)" % sys.argv[2])

    else:
        print pipe_count("moby-dic.txt")
