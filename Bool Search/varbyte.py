import struct

def code_to_bin_one_number(i, f):
    depth = 1
    if i < 128:
        f.write(struct.pack('B', i + 128))
        return depth
    else:
        i_rem = i % 128
        i_degr =  i // 128
        depth = code_to_bin_i_degr(i_degr, f, depth)
        f.write(struct.pack('B', i_rem + 128))
        return depth

def code_to_bin_i_degr(i, f, depth):
    depth += 1
    if i < 128:
        f.write(struct.pack('B', i))
    else:
        i_rem = i % 128
        i_degr =  i // 128
        depth = code_to_bin_i_degr(i_degr, f, depth)
        f.write(struct.pack('B', i_rem))
    return depth

def code_varbyte(list_, f):
    bytes = 0
    for s in list_:
        bytes += code_to_bin_one_number(s, f)
    return bytes

def decode_one_number(f):
    val = struct.unpack('B', f.read(1))[0]
    if val >= 128:
        return val - 128
    else:
        return decode_next_byte(val, f)

def decode_next_byte(i, f):
    val = struct.unpack('B', f.read(1))[0]
    if val >= 128:
        return 128 * i + val - 128
    else:
        return decode_next_byte(128 * i + val, f)

def decode_varbyte(f_offset, N):
    l = []
    for i in range(N):
        l += [decode_one_number(f_offset)]
    return l

def code_to_diff(list_):
    l = []
    l += [list_[0]]
    for i in range(len(list_) - 1):
        l += [list_[i + 1] - list_[i]]
    return l

def decode_unto_diff(list_):
    l = []
    l += [list_[0]]
    for i in range(len(list_) - 1):
        l += [l[i] + list_[i + 1]]
    return l