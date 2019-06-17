import os
import array

from .helpers import MAX_BITS
from .serialize_modes import serialize_modes


class Decoder(object):
    def __init__(self, filename=None, encode_mode=None, serialize_mode=None, raw_str=None):
        self.encode_mode = encode_mode or 0
        self.serialize_mode = serialize_mode or 0
        if filename and os.path.exists(filename):
            with open(filename, 'rb') as f:
                self.parse_data(f.read())
        elif filename:
            print('Файл {} не найден'.format(filename))
            raise NotImplementedError()
        elif raw_str:
            self.parse_data(raw_str)
        else:
            print('Выберите хотябы 1 параметр.')
            raise NotImplementedError()

    def parse_data(self, raw_data):
        serializer = serialize_modes.get(self.serialize_mode)
        if not serializer:
            raise NotImplementedError()

        lib1 = serializer['lib1']
        lib2 = serializer['lib2']
        data, length, array_codes = lib2.loads(raw_data)
        self.root = lib1.loads(data)
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

    def decode_as(self, filename):
        decoded = self._decode()
        with open(filename, 'wb') as f:
            f.write(decoded)
