#!/bin/python3

import math
import os
import random
import re
import sys

from functools import cmp_to_key
class Player:
    def __init__(self, name, score):
        self.name = name
        self.score = score
        
    def __repr__(self):
        pass
        
    def comparator(a, b):
        if a.score > b.score:
            return -1

        elif a.score < b.score:
            return 1

        else: # scores are equal, compare based on name
            if a.name < b.name:
                return -1
            elif a.name > b.name:
                return 1
            else:
                return 0


if __name__ == '__main__':
    output_to_file = False
    s_f_index = '07'
    base_path = './InterviewPrepKit/Sorting/Comparator/'
    fname_input = base_path + f'input{s_f_index}.txt'
    fname_expect = base_path + f'output{s_f_index}.txt'

    print(f"\ntesting against input file {fname_input}...")

    fd = open(fname_input)
    sys.stdin = fd

    f_expect = open(fname_expect)
    f_debug = None
    if output_to_file:
        f_debug = open(base_path+f'debug-output{s_f_index}.txt', 'w')
        sys.stdout = f_debug




    n = int(input())
    data = []
    for i in range(n):
        name, score = input().split()
        score = int(score)
        player = Player(name, score)
        data.append(player)
        
    data = sorted(data, key=cmp_to_key(Player.comparator))
    # for i in data:
    #     print(i.name, i.score)
    result = [f"{i.name} {i.score}" for i in data]




    expect = f_expect.readlines()
    for i, l in enumerate(expect):
        _expect = l.strip()
        print(f"expect: {_expect}")
        s_result = None
        if i < len(result):
            s_result = str(result[i])
            print(f"result: {s_result}")
        else:
            print(f"result: <non-existence... result only has {len(result)} elements>")
        if _expect != s_result:
            print(f"failed on result index: {i}")
        assert(_expect == s_result)
        print()

    fd.close()
    f_expect.close()

    if output_to_file:
        f_debug.close()
        sys.stdout = sys.__stdout__

    sys.stdin = sys.__stdin__    # Reset the stdin to its default value
