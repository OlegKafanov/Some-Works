import re

def cut_sorted(ext, min_value):
    z = []
    for i in range(len(ext)):
        if ext[i][1] > min_value:
            z += [ext[i]]
        else:
            return z
    return z

def count(lst):
    dct = {}
    for i in lst:
        if i in dct:
            dct[i] += 1
        else:
            dct[i] = 1
    return dct

class Tree:
    def __init__(self, left, right):
        self.token = 0
        self.left = left
        self.right = right


def parse_query(factors):
    if (factors[0] == '(') & (factors[len(factors) - 1] == ')'):
        factors = factors[1:len(factors)]
    number = 0
    bracket = 0
    factor_number = 1000
    factor_min = None
    factor_pos = 0
    i = 0
    for factor in factors:
        #print factor
        if (factor == '('):
            bracket += 2
        elif (factor == ')'):
            bracket -= 2
        elif (factor == '&') | (factor == u'|') | (factor == u'!'):
            #print factor

            if factor == '&':
                number = 2
            elif factor == '|':
                number = 1
            elif factor == '!':
                number = 3

            if number + bracket <= factor_number:
                factor_min = factor
                factor_number = number + bracket
                factor_pos = i
        i += 1
    if factor_min:
        right_str = []
        left_str = []
        for i in range(len(factors)):
            if i < factor_pos:
                left_str += [factors[i]]
            elif i > factor_pos:
                right_str += [factors[i]]

        token = factors[factor_pos]
        left = left_str
        right = right_str
    else:
        token = factors[0]
        left = None
        right = None

    return [token, left, right]


def split_query(query):
    #str_ = ''
    #for i in reversed(sorted(re.split(re.compile(r'&', re.U), query))):
    #    str_ += i + "&"
    #new_query = str_[:-1]

    TOKS = re.compile(r'\w+|[\(\)&\|!]', re.U)
    return re.findall(TOKS, query)

def build_tree(tree, factors):
    parse = parse_query(factors)
    tree.token = parse[0]
    if parse[1]:
        tree.left = Tree(None, None)
        build_tree(tree.left, parse[1])
    else:
        tree.left = None
    if parse[2]:
        tree.right = Tree(None, None)
        build_tree(tree.right, parse[2])
    else:
        tree.right = None

def go_around_tree(tree):
    print tree.token
    if tree.left:
        go_around_tree(tree.left)
    if tree.right:
        go_around_tree(tree.right)
    #print tree.token

def bind_index_to_leafs(tree, back_descr):
    if (tree.token == u'&') | (tree.token == u'|') | (tree.token == u'!'):
        if (tree.token == u'!'):
            bind_index_to_leafs(tree.right, back_descr)
        else:
            bind_index_to_leafs(tree.left, back_descr)
            bind_index_to_leafs(tree.right, back_descr)
    else:
        #tree.token = back_descr[tree.token]
        tree.token = set(back_descr[tree.token])
#        print tree.token

def execute_tree(tree):
    if (tree.token == u'&') | (tree.token == u'|') | (tree.token == u'!'):
        if (tree.token == u'!'):
            return tree.token
        #    tree.token = set([x for x in range(1, max_descr + 1)]).difference(set(back_descr[tree.right.token]))
        if (tree.left.left == None) & (tree.left.right == None) & (tree.right.left == None) & (tree.right.right == None):
            if tree.token == u'&':
                tree.token = tree.left.token & tree.right.token
            elif tree.token == '|':
                tree.token = tree.left.token | tree.right.token
            #if tree.token == '!':

            #!!!!!!!!!!!!!!!!!!!
        else:
            if (tree.left.left != None) | (tree.left.right != None):
                execute_tree(tree.left)
            if (tree.right.left != None) | (tree.right.right != None):
                execute_tree(tree.right)

            if (tree.token == u'&'):
                if ((tree.left.token == u'!') | (tree.right.token == u'!')):
                    if (tree.left.token == u'!'):
                        tree.token = tree.right.token.difference(tree.left.right.token) #'!' always before word
                    else: #there is not double '!'
                        tree.token = tree.left.token.difference(tree.right.right.token)  # '!' always before word
                else:
                    tree.token = tree.left.token & tree.right.token
            elif (tree.token == u'|'):
                tree.token = tree.left.token | tree.right.token

    return tree.token

def stream_execute_tree(tree, cur_docID):
    if (tree.token == u'&') | (tree.token == u'|') | (tree.token == u'!'):
        if (tree.token == u'&') & (tree.right.token == u'!'):
            left_list = stream_execute_tree(tree.left, cur_docID)
            if left_list:
                right_list = stream_execute_tree(tree.right, [cur_docID, left_list[0]]) #+LEFT_LIST[0]!!!!!!!!1
            else:
                return []
        elif (tree.token == u'&') | (tree.token == u'|'):
            left_list = stream_execute_tree(tree.left, cur_docID)
            right_list = stream_execute_tree(tree.right, cur_docID)
        else:
            left_list = [] #so that the interpreter/IDE does not swear
            right_list = stream_execute_tree(tree.right, cur_docID[0]) #see 6 strings up ^
    else:
        for i in tree.token:
            if i < cur_docID:
                tree.token = tree.token[1:]
            else:
                break
        #print tree.token
        return tree.token

    if (tree.token == u'&'):
        if (left_list == []) | (right_list == []):
            return []
        #return [max(left_list[0], right_list[0])]
        if left_list[0] > right_list[0]:
            more = left_list
            less = right_list
        else:
            more = right_list
            less = left_list
        for i in less:
            if i == more[0]:
                return [i]
            if i > more[0]:
                #print i, more[0]
                while (i > more[0]):
                    more = more[1:]
                    if more == []:
                        return []
                if i == more[0]:
                    return [i]
                #print "!", more[0]

        return []

    elif (tree.token == u'|'):
        if (left_list == []) & (right_list == []):
            return []
        if (left_list == []):
            return [right_list[0]]
        if (right_list == []):
            return [left_list[0]]
        #print min(left_list[0], right_list[0])
        return [min(left_list[0], right_list[0])]

    elif (tree.token == u'!'):
        if right_list == []:
            return [cur_docID[1]]
        for i in right_list:
            if i == cur_docID[1]:
                return []
            elif i > cur_docID[1]:
                break
        return [cur_docID[1]]
