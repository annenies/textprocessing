import os
import re
import string
import sqlite3
import random

filez = []
bookid = []
ibws = dict()

for root, dirs, files in os.walk("excerpts/"):
    for name in files:
        if name.endswith((".txt")):
            filez.append(root + name)
            bid = re.findall('[0-9]*', name)
            for i in range(len(bid)):
                if len(bid[i]) > 0:
                    bookid.append(bid[i])


for i in range(len(filez)):
    f = open(filez[i], 'r')
    ewords = []
    for line in f:
        ewords.extend(re.sub('[' + string.punctuation + ']', ' ', line).split())

    ewordss = set(ewords)
    ewords = list(ewordss)
    ewords.sort()

    e = dict()

    conn = sqlite3.connect('e_test.sqlite3')
    cur = conn.cursor()
    cur.execute('SELECT word, wordrank FROM Words')

    for word, wordrank in cur:
        if word in ewords:
            e[word] = wordrank

    l = []
    ibw = []

    for key in e:
        l.append(e[key])

    for key in e:
        if e[key] == max(l):
            ibw.append(key)
    if len(ibw)>0:
        x = random.randint(0, len(ibw)-1)
        w = ibw[x]
    else: continue

    cur.execute('SELECT WordID FROM Words WHERE word=?', (w,))

    for WordID in cur:
        wid = WordID[0]

    ibws[bookid[i]] = wid

print ibws

for key in ibws:
    cur.execute('UPDATE Excerpts SET wordid=? WHERE ebookid=?', (ibws[key], key))

conn.commit()