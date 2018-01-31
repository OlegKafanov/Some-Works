
import json
import codecs
from binary_dict import HashCoder
from url_bin import BinUrl

f = codecs.open("term_dict",'r','utf-8')
dict_index = json.load(f)
f.close()

f = open('term_hash', 'w')
h = HashCoder(f, 3 * len(dict_index) // 2)
for word in dict_index:
    h.put(word, dict_index[word])

dict_index = {}
h.write_to_file()
f.close()

#URLS
f = open("url_list",'r')
url_list = json.load(f)
f.close()

#print url_list
f = open('urls', 'w')
bu = BinUrl(url_list, f)
bu.code()
f.close()

#f = open('maxID','w')
#f.write(str(len(url_list)))
#f.close()
