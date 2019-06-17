import os
import array
import marshal
import pickle

from .model import H
from .helpers import (
    build_tree,
    get_frequency_table,
    generate_huffman_code,
    MAX_BITS,
)


class Encoder(object):

    def remove_padding(self, text):
        padded_info = text[:8]
        extra_padding = int(padded_info, 2)

        padded_encoded_text = text[8:]
        encoded_text = padded_encoded_text[:-1 * extra_padding]

        return encoded_text

    def __init__(self, filename=None, encode_mode=None, serialize_mode=None, long_str=None):
        self._long_str = ''
        self.encode_mode = encode_mode or 0
        self.serialize_mode = serialize_mode or 0
        if filename and os.path.exists(filename):
            with open(filename, 'rb') as f:
                self.long_str = f.read()
        elif filename:
            print('File {} does not exists'.format(filename))
        elif long_str:
            self.long_str = long_str
        else:
            print('Please specify params.')

    @property
    def long_str(self):
        return self._long_str

    @long_str.setter
    def long_str(self, s):
        self._long_str = s
        if s:
            self.root = self._get_tree_root()
            self.code_map = self._get_code_map()
            if self.encode_mode == 0:
                encode_func = self._encode_as_bytes
            elif self.encode_mode == 1:
                encode_func = self._encode_as_string
            self.array_codes, self.code_length = encode_func()

    def _get_tree_root(self):
        _frequency_table = get_frequency_table(self.long_str)
        return build_tree(
            [H(char=char, frequency=int(frequency)) for char, frequency in _frequency_table.items()]
        )

    def _get_code_map(self):
        a_dict = {}
        generate_huffman_code(self.root, a_dict)
        m = 0
        for i in a_dict.values():
            m = max(m, len(i))
        print(m)
        return a_dict

    def _encode_as_bytes(self):
        array_codes = array.array('B')
        code_length, buff, length = 0, 0, 0
        codes = ''
        for ch in self.long_str:
            code = self.code_map[ch]
            codes += code
            for bit in code:
                if bit == '1':
                    buff = (buff << 1) | 0x01
                else:
                    buff = (buff << 1)
                length += 1
                if length == MAX_BITS:
                    # array_codes.extend([buff])
                    array_codes.append(buff)
                    buff, length = 0, 0

            code_length += len(code)

        b = bytearray()
        for i in range(0, len(codes), 8):
            byte = codes[i:i + 8]
            b.append(int(byte, 2))
        return b, code_length
        print(b)


        if length != 0:
            array_codes.extend([buff << (MAX_BITS - length)])
        print(array_codes)
        return array_codes, code_length

    def _encode_as_string(self):
        encoded_string = ''
        for ch in self.long_str:
            encoded_string += self.code_map[ch]
        return encoded_string, len(encoded_string)

    def write(self, filename):
        if self._long_str:
            fcompressed = open(filename, 'wb')
            fcompressed.write(bytes(self.array_codes))
            # marshal.dump(
            #     (pickle.dumps(self.root), self.code_length, self.array_codes),
            #     fcompressed)
            # fcompressed = open(filename + '2', 'wb')
            # pickle.dump(
            #     (pickle.dumps(self.root), self.code_length, self.array_codes),
            #     fcompressed)
            # fcompressed.close()
        else:
            print("Please set long_str.")
