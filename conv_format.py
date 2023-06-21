"""Sadaf Khan, LING570, HW8, 11/27/2021. Converts Viterbi output to another format."""

import sys
import re

for line in sys.stdin:
    line = line.split("=>")
    words = line[0].split()
    tags_prob = line[1].split()
    prob = tags_prob[-1]
    two_tags = tags_prob[1:-1]
    tags = []
    for pair in two_tags:
        new = re.sub(r'^.*?_',"", pair)
        tags.append(new)
    sequence = list(zip(words,tags))
    for (word, tag) in sequence:
        print(word + "/" + tag + " ", end='')
    print("\n")
