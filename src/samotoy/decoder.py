import os
import array
import marshal
import pickle

from .helpers import MAX_BITS


class Decoder(object):
    def __init__(self, filename=None, encode_mode=None, serialize_mode=None, raw_str=None):
        self.encode_mode = encode_mode or 0
        self.serialize_mode = serialize_mode or 0
        if filename and os.path.exists(filename):
            with open(filename, 'rb') as f:
                self.parse_data(*marshal.load(f))
        elif filename:
            print('File {} does not exists'.format(filename))
            raise NotImplementedError()
        elif raw_str:
            self.parse_data(*marshal.loads(raw_str))
        else:
            print('Please specify params.')
            raise NotImplementedError()

    def parse_data(self, data, length, array_codes):
        self.root = pickle.loads(data)
        self.code_length = length
        self.array_codes = array.array('B', array_codes)

    def _decode(self):
        string_buf = array.array('B')
        total_length = 0
        node = self.root
        for code in self.array_codes:
            buf_length = 0
            while (buf_length < MAX_BITS and total_length != self.code_length):
                buf_length += 1
                total_length += 1
                if code >> (MAX_BITS - buf_length) & 1:
                    node = node.R
                    if node.C is not None:
                        string_buf.append(node.C)
                        node = self.root
                else:
                    node = node.L
                    if node.C is not None:
                        string_buf.append(node.C)
                        node = self.root

        return string_buf

    def read(self, filename):
        fp = open(filename, 'rb')
        unpickled_root, length, array_codes = marshal.load(fp)
        self.root = pickle.loads(unpickled_root)
        self.code_length = length
        self.array_codes = array.array('B', array_codes)
        fp.close()

    def decode_as(self, filename):
        decoded = self._decode()
        fout = open(filename, 'wb')
        fout.write(decoded)
        fout.close()
