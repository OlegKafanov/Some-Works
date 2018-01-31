# -*- coding: utf-8 -*-

import doc_reader
from doc2words import extract_words
import json
import codecs
from varbyte import code_varbyte, code_to_diff
from simple9 import code_simple9
import time


descriptor_back = {}
term_dict = {}
url_list = []
i = 1

for data in doc_reader.parse_command_line().files:
    docs = []
    reader = doc_reader.DocumentStreamReader([data])
    for doc in reader:
        docs += [doc]

    for doc in docs:
        descriptor_back[i] = doc
        url_list += [doc.url]
        words = set(extract_words(doc.text))
        for word in words:
            if word in term_dict:
                term_dict[word] += [i]
            else:
                term_dict[word] = [i]
        i += 1
docs = []

#create index
dict_index = {}
offset = 0
f = open('index','w')
f_coding = open('coding','r')
coding = f_coding.read()

t = []
t += [time.time()]

if coding == 'varbyte':
    for word in term_dict:
        dict_index[word] = [offset, len(term_dict[word])]
        offset += code_varbyte(code_to_diff(term_dict[word]), f)

elif coding == 'simple9':
    for word in term_dict:
        dict_index[word] = [offset, len(term_dict[word])]
        offset += 4 * code_simple9(code_to_diff(term_dict[word]), f)

t += [time.time()]

f_coding.close()
f.close()

term_dict = {}

#dump dicts
f = codecs.open("term_dict",'w', "utf-8")
json.dump(dict_index, f)
f.close()

f = open("url_list",'w')
json.dump(url_list, f)
f.close()
