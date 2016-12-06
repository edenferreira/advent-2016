import json
from itertools import groupby
from operator import itemgetter

def counting_equals(l):
    counted = {}
    for e in l:
        if e in counted:
            counted[e] += 1
        else:
            counted[e] = 0
    return counted

with open('day-6-input.json') as f:
    data = json.load(f)
    listOflists = (list(w) for w in data)
    transposed = zip(*listOflists)
    counted = (counting_equals(t) for t in transposed)
    messageAsList = (max(d.items(), key=itemgetter(1))[0] for d in counted)
    print(''.join(messageAsList))

