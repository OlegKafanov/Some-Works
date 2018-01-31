import struct

SIZE_OF_CELL = 48
TECH_INFO = 4


class HashCoder:
    def __init__(self, file_, table_size):
        self.file_ = file_
        self.table_size = table_size

        self.keys = [None] * table_size
        self.values = [None] * table_size

    def put(self, key, value):
        hash_val = self.hash_(key)
        if self.keys[hash_val] == None:
            self.keys[hash_val] = key
            self.values[hash_val] = value
        else:
            i = 1
            next_cell = self.re_hash(hash_val, i)
            while self.keys[next_cell] != None:
                i += 1
                next_cell = self.re_hash(next_cell, i)

            self.keys[next_cell] = key
            self.values[next_cell] = value

    def hash_(self, key):
        l = len(key)
        if l > 10:
            l += 1
        w = self.table_size / 2 + (self.table_size / 2) * ((2 * (l % 11) - 12) / 10.)

        sum_ = 0
        for i in range(len(key)):
            sum_ = sum_ + (i + 3) * ord(key[i])

        return int(w + sum_ % (self.table_size / 10))

    def re_hash(self, old_hash, i):
        return (old_hash + 111111) % self.table_size  # linear shift

    def write_to_file(self):
        self.file_.write(struct.pack('I', self.table_size))  # TECH_INFO
        for j in range(self.table_size):
            self.file_.seek(TECH_INFO + SIZE_OF_CELL * j)
            if self.keys[j] != None:
                for char in self.keys[j]:
                    self.file_.write(struct.pack('H', ord(char)))
                if len(self.keys[j]) < 20:
                    self.file_.write(struct.pack('H', 0))
                # else: if > 20: very large word!!!
                self.file_.seek(TECH_INFO + SIZE_OF_CELL * j + 40)
                self.file_.write(struct.pack('I', self.values[j][0]))
                self.file_.write(struct.pack('I', self.values[j][1]))
            else:
                self.file_.write(struct.pack('H', 0))
'''
    def hash_(self, key):
        sum_ = 0
        for i in range(len(key)):
            sum_ = sum_ + (i + 3) * ord(key[i])

        return sum_ % self.table_size
'''

class HashDecoder:
    def __init__(self, file_):
        self.file_ = file_
        self.table_size = struct.unpack('I', self.file_.read(4))[0]

    def get(self, key):
        hash_val = self.hash_(key)
        self.file_.seek(hash_val * SIZE_OF_CELL)
        if self.read_key(hash_val) == key:
            return self.read_value(hash_val)
        else:
            while (1):  # SIMPLE NUMBER OF TABLE SIZE ???
                hash_val = self.re_hash(hash_val)
                if self.read_key(hash_val) == key:
                    return self.read_value(hash_val)

                    # while self.keys[position] != key

    def read_key(self, offset):
        self.file_.seek(TECH_INFO + SIZE_OF_CELL * offset)
        word = ''
        for i in range(20):
            val = struct.unpack('H', self.file_.read(2))[0]
            if val == 0:
                break
            word += unichr(val)
        return word

    def read_value(self, offset):
        self.file_.seek(TECH_INFO + SIZE_OF_CELL * offset + 40)
        list_ = []
        list_ += [struct.unpack('I', self.file_.read(4))[0]]
        list_ += [struct.unpack('I', self.file_.read(4))[0]]
        return list_

    def hash_(self, key):
        l = len(key)
        if l > 10:
            l += 1
        w = self.table_size / 2 + (self.table_size / 2) * ((2 * (l % 11) - 12) / 10.)

        sum_ = 0
        for i in range(len(key)):
            sum_ = sum_ + (i + 3) * ord(key[i])

        return int(w + sum_ % (self.table_size / 10))

    def re_hash(self, old_hash):
        return (old_hash + 111111) % self.table_size  # linear shift

'''
    def hash_(self, key):
        sum_ = 0
        for i in range(len(key)):
            sum_ = sum_ + (i + 3) * ord(key[i])

        return sum_ % self.table_size
'''