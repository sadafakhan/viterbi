"""Sadaf Khan, LING570, HW8, 11/22/2021. Reads in an HMM model, stores it, and implements the Viterbi algorithm."""

import os
import re
import sys
import numpy as np
from nltk.tokenize import word_tokenize

with open(sys.argv[1], "r") as f:
    unformatted_hmm = f.readlines()

# get information from the raw data, separate it into sections as needed
n = int(re.sub(".*\=","", unformatted_hmm[1]))
unformatted_hmm = unformatted_hmm[7:]
unformatted_sections = []

i = 0
j_holder = 0
for j in range(0, len(unformatted_hmm)):
    if unformatted_hmm[j].startswith("\\"):
        if j == 0:
            pass
        else:
            section = unformatted_hmm[i:j]
            unformatted_sections.append(section)
            i = j
            j_holder = j

init_old = unformatted_sections[0]
trans_old = unformatted_sections[1]
emiss_old = unformatted_hmm[j_holder:len(unformatted_hmm)]

# create reference books for state identities
state2num = {}
num2state = {}
id_counter = 0
sym2num = {}
num2sym = {}

for item_raw in trans_old:
    if item_raw == "\n" or item_raw == "\t\n" or item_raw.startswith("\\transition\n"):
        pass
    else:
        item = item_raw.strip().split("\t")[:2]
        start_state = item[0]
        end_state = item[1]
        for state in [start_state, end_state]:
            if state not in state2num:
                state2num[state] = id_counter
                num2state[id_counter] = state
                id_counter += 1

#reset id counter
id_counter = 0

for item_raw in emiss_old:
    if item_raw == "\n" or item_raw == "\t\n" or item_raw.startswith("\\emission\n"):
        pass
    else:
        item = item_raw.strip().split("\t")
        symbol = item[1]

        if symbol not in sym2num:
            sym2num[symbol] = id_counter
            num2sym[id_counter] = symbol
            id_counter += 1

k = len(state2num)

# starting state probabilities; likely just BOS_BOS = 1.0, but just in case
pi = np.zeros([k,])
for item in init_old:
    if item == "\n" or item == "\t\n" or item.startswith("\\init\n"):
        pass
    else:
        item = item.strip().split()
        state = state2num[item[0]]
        prob = float(item[1])
        pi[state] = prob

# transition array that will be populated as (start state, end state = prob)
a = np.zeros([k,k])

for item_raw in trans_old:
    if item_raw == "\n" or item_raw == "\t\n" or item_raw.startswith("\\transition\n"):
        pass
    else:
        item = item_raw.strip().split("\t")[:3]
        start_state = state2num[item[0]]
        end_state = state2num[item[1]]
        prob = float(item[2])
        # lg_prob = float(item[3])
        a[start_state, end_state] = prob

b = np.zeros([k,n])

for item_raw in emiss_old[0:15]:
    if item_raw == "\n" or item_raw == "\t\n" or item_raw.startswith("\\emission\n"):
        pass
    else:
        item = item_raw.strip().split("\t")
        emitter = state2num[item[0]]
        symbol = sym2num[item[1]]
        prob = float(item[2])
        unk_prob = float(item[-1].split(" ")[-1].split("=")[-1])

        b[emitter, symbol] = prob
        # print(item[0],emitter,item[1],symbol,prob)

        if unk_prob > 0:
            b[emitter, sym2num["<UNK>"]] = unk_prob


def step(mu_prev, b, a, observed_state):
    pre_max = mu_prev * a.T
    max_prev_states = np.argmax(pre_max, axis=1)
    max_vals = pre_max[np.arange(len(max_prev_states)), max_prev_states]
    mu_new = max_vals * b[:, observed_state]
    return mu_new, max_prev_states

def viterbi(b, a, pi, observation):

    # forward pass
    mu = pi * b[:, observation[0]]

    all_prev_states = []

    for observed_state in observation[1:]:
        mu, prevs = step(mu, b, a, observed_state)
        all_prev_states.append(prevs)

    # tracing backwards
    state = np.argmax(mu)
    order_prob = mu[state]
    state_order = [state]
    for prev_states in all_prev_states[::-1]:
        state = prev_states[state]
        state_order.append(state)

    return state_order[::-1], order_prob

tests = open(os.path.join(os.path.dirname(__file__), sys.argv[2]), 'r').read().split("\n")[:-1]
observation_words = word_tokenize(tests[0])

observation = [0]
for word in observation_words:
    if word not in sym2num:
        word = "<unk>"
    observation.append(sym2num[word])


with open(sys.argv[3], "w") as g:
    # observ => state seq lgprob
    for test in tests:
        observation_words = word_tokenize(test)
        observation = [0]
        for word in observation_words:
            if word not in sym2num:
                word = "<unk>"
            observation.append(sym2num[word])

        result = viterbi(b, a, pi, observation)

        g.write(test + " => " + str(' '.join(map(str, result[0]))) + "\t"+ str(result[1]))
        g.write("\n")
