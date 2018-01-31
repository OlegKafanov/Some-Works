import struct

class BitstreamWriter:
    def __init__(self):
        self.nbits  = 0
        self.curbyte = 0
        self.vbytes = []

    """ add single bit """
    def add(self, x):
        self.curbyte |= x << (8-1 - (self.nbits % 8))
        self.nbits += 1

        if self.nbits % 8 == 0:
            self.vbytes.append(chr(self.curbyte))
            self.curbyte = 0

    """ get byte-aligned bits """
    def getbytes(self):
        if self.nbits & 7 == 0:
            return "".join(self.vbytes)

        return "".join(self.vbytes) + chr(self.curbyte)


class BitstreamReader:
    def __init__(self, blob):
        self.blob = blob
        self.pos  = 0

    """ extract next bit """
    def get(self):
        ibyte = self.pos / 8
        ibit  = self.pos & 7

        self.pos += 1
        return (ord(self.blob[ibyte]) & (1 << (7 - ibit))) >> (7 - ibit)

    def finished(self):
        return self.pos >= len(self.blob) * 8


def number_to_binary_code(num, n_bits, bsw):
    l = []
    for i in range(n_bits):
        l += [num & 1]
        num = num >> 1
    for i in l[::-1]:
        bsw.add(i)


def read_number_from_binary_code(n_bits, bsr):
    x = 0
    for i in range(n_bits):
        x = x << 1 | bsr.get()
    return x


def code_simple9(list_, f):
    code_len = 0
    while(len(list_)):
        code_len += 1
        i = 0
        k = [28,14,9,7,5,4,3,2,1]
        for i in range(9):
            if len(list_) >= k[i]:
                if max(list_[:k[i]]) < 2**k[8-i]: #<=!!!! 0 = 2**k[8-i]
                    bs = BitstreamWriter()
                    number_to_binary_code(i, 4, bs)
                    for j in range(k[i]):
                        number_to_binary_code(list_[j], k[8-i], bs)
                    list_ = list_[k[i]:]
                    for byte in bs.getbytes():
                        f.write(struct.pack('c', byte))
                    break
            elif max(list_) < 2**k[8-i]: #<=!!!! 0 = 2**k[8-i]
                bs = BitstreamWriter()
                number_to_binary_code(i, 4, bs)
                for j in range(len(list_)):
                    number_to_binary_code(list_[j], k[8-i], bs)
                list_ = list_[k[i]:]
                for byte in bs.getbytes():
                    f.write(struct.pack('c', byte))
                if len(bs.getbytes()) < 4:
                    for j in range(4 - len(bs.getbytes())):
                        f.write(struct.pack('c', '0'))
                break
    return code_len

def decode_simple9(f, n_numbers):
    k = [28,14,9,7,5,4,3,2,1]
    list_ = []
    n = 0
    while(n < n_numbers):
        str_ = ''
        for i in range(4):
            str_ += struct.unpack('c', f.read(1))[0]
        bsr = BitstreamReader(str_)
        i = read_number_from_binary_code(4, bsr)
        for j in range(k[i]):
            if n < n_numbers:
                list_ += [read_number_from_binary_code(k[8 - i], bsr)]
                n += 1
            else:
                return list_
    return list_