# -*- coding: utf-8 -*-

import sys
import lib
from varbyte import decode_varbyte, decode_unto_diff
from simple9 import decode_simple9
from binary_dict import HashDecoder
from url_bin import DecBinUrl

query_original = sys.argv[1].decode('utf-8')
query = query_original.lower()

#extract words from query
words = []
for i in lib.split_query(query):
    if (i != u'&') & (i != u'|') & (i != u'!') & (i != u'(') & (i != u')'):
        words += [i]

#decode some words from dict
term_dict = {}
f = open('term_hash', 'r')
h = HashDecoder(f)
i = 0
for word in words:
    term_dict[word] = h.get(word)
f.close()

#decode some lists from index
f = open('index','r')
f_coding = open('coding','r')
coding = f_coding.read()
back_descr = {}

if coding == 'varbyte':
    for word in words:
        f.seek(int(term_dict[word][0]))
        back_descr[word] = decode_unto_diff(decode_varbyte(f, int(term_dict[word][1])))

elif coding == 'simple9':
    for word in words:
        f.seek(int(term_dict[word][0]))
        back_descr[word] = decode_unto_diff(decode_simple9(f, int(term_dict[word][1])))

f_coding.close()
f.close()

#build and execute tree
tree = lib.Tree(None, None)

lib.build_tree(tree, lib.split_query(query))

lib.bind_index_to_leafs(tree, back_descr)

answer = sorted(lib.execute_tree(tree))

#f = open('maxID','r')
#maxID = int(f.read())
#f.close()
'''
ends = []
for i in back_descr:
    ends += [back_descr[i][-1]]

maxID = 0
if len(ends) > 1:
    for i in range(len(ends) - 1):
        if ends[i + 1] > ends[i]:
            maxID = ends[i + 1]
        else:
            maxID = ends[i]
else:
    maxID = ends[0]
list_execute = []


docID = -1
while (docID < maxID):
    val = lib.stream_execute_tree(tree, docID)
    if val == []:
        docID += 1
        #break
    else:
        list_execute += [val[0]]
        docID = val[0] + 1

answer = sorted(list_execute)
'''

#output
print query_original.encode('utf-8')
print len(answer)
f = open('urls','r')
dec = DecBinUrl(f)
for i in answer:
    print dec.decode(i - 1)
