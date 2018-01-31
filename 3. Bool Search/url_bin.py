import struct

class BinUrl:
    def __init__(self, list_, file_):
        self.list_ = list_
        self.file_ = file_

    def code(self):
        i = 0
        for url in self.list_:
            url.encode('ascii')
            for char in url:
                self.file_.write(struct.pack('B', ord(char)))
            self.file_.write(struct.pack('b', 0))
            i += 1
            self.file_.seek(256 * i)


class DecBinUrl:
    def __init__(self, file_):
        self.file_ = file_

    def decode(self, offset):
        self.file_.seek(256 * offset)
        str_ = ''
        for i in range(256):
            val = chr(struct.unpack('B', self.file_.read(1))[0])
            if val != '\0':
                str_ += val
            else:
                return str_
        return str_