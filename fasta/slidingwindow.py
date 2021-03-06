"""
Scans a user-provided FASTA file using a user-defined sliding window width.
Each chunks, however, has overlap much like scaffolding sequences. Such a
scenario is useful for instances where you wish to perform genome-wide
predictions on an entire genome.
"""

import argparse
from Bio import SeqIO


def parse_fasta(f):
    """
    Parses a user-provided FASTA file.
    @param f: FASTA file.
    @return: collection of FASTA entries.
    """
    records = SeqIO.parse(f, 'fasta')
    return records


def get_n_perc(seq):
    """
    Derive the N % of a sequence.
    @param seq: DNA sequence.
    @return: percentage representing the N percentage.
    """
    n_count = float(str(seq).upper().count('N'))
    return n_count / len(seq) * 100


def run_slidingwindow(f, w, o, n):
    """
    Runs the logic of the sliding window algorithm with overlapping segments.
    @param f: User-provided input FASTA file.
    @param w: Sliding window size.
    @param o: Sliding window overlap size.
    @param n: Hard-mask threshold; ignore sequences exceeding this value.
    """
    entries = parse_fasta(f)
    for entry in entries:
        seq = str(entry.seq)
        d = entry.description  # sequence descriptor
        chunk1 = seq[0: w]  # the first chunk has no overlaps
        start, end = 0, w
        if get_n_perc(chunk1) < n:
            print('>' + d + '|' + str(start) + '|w|' + str(w) + '|o|' + str(o))
            print(chunk1)
        while True:
            start = end - o
            end = start + w
            win = seq[start: end]
            if start > len(seq):
                break
            if start != len(seq) and get_n_perc(win) < n:
                print('>' + d + '|' + str(start) + '|w|' + str(w) + '|o|' + str(o))
                print(win)

if __name__ == '__main__':
    desc = 'Trivial sliding window algorithm with overlap amongst segments.'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-f', metavar='FASTA', help='FASTA file [req]',
                        required=True)
    parser.add_argument('-w', metavar='INT', help='Sliding window width [100]',
                        default=100, type=int)
    parser.add_argument('-o', metavar='INT', help='Window overlap [30]',
                        default=30, type=int)
    parser.add_argument('-n', metavar='INT', help='Ignore windows > N pct [50]',
                        default=50, type=int)
    args = vars(parser.parse_args())
    try:
        if args['w'] <= args['o']:
            raise IOError('Window size must be > overlap size.')
        run_slidingwindow(f=args['f'], w=args['w'], o=args['o'], n=args['n'])
    except IOError as e:
        print(e)
