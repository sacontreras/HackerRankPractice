#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'checkMagazine' function below.
#
# The function accepts following parameters:
#  1. STRING_ARRAY magazine
#  2. STRING_ARRAY note
#

def checkMagazine(magazine, note):
    debug = True

    if debug:
        print(f"magazine: {magazine}")
        print(f"note: {note}")

    d_magazine = {}
    for w in magazine:
        d_magazine[w] = d_magazine.get(w,0) + 1
    d_note = {}
    for w in note:
        d_note[w] = d_note.get(w,0) + 1

    if debug:
        print(f"d_magazine: {d_magazine}")
        print(f"d_note: {d_note}")

    for w_note, n_w_note in d_note.items():
        if w_note not in d_magazine.keys():
            print("No")
            return

        n_w_magazine = d_magazine[w_note]
        if n_w_note > n_w_magazine:
            print("No")
            return

    # if we are here then the ransom note can be created from the magazine
    print("Yes")


if __name__ == '__main__':
    fname_input = './InterviewPrepKit/Dictionaries/HashTables-RansomNote/' + 'input03.txt'
    print(f"testing against input file {fname_input}")

    fd = open(fname_input)
    sys.stdin = fd

    first_multiple_input = input().rstrip().split()

    m = int(first_multiple_input[0])

    n = int(first_multiple_input[1])

    magazine = input().rstrip().split()

    note = input().rstrip().split()

    checkMagazine(magazine, note)

    sys.stdin = sys.__stdin__    # Reset the stdin to its default value
