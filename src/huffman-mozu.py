
from collections import defaultdict
import os
import array
import marshal
import pickle


class H:

    def __init__(self, char=None, frequency=None, left_node=None, right_node=None, print_char=None):
        self.C = char
        self.F = frequency
        self.L = left_node
        self.R = right_node

    def __repr__(self):
        return ''.join([self.C or 0x00, str(self.frequency), str(self.L or 0x00), str(self.R or 0x00)])

    def __gt__(self, other):
        if not isinstance(other, HuffmanNode):
            return super(HuffmanNode, self).__gt__(other)
        return self.F < other.F

class HuffmanNode:

    def __init__(self, char=None, frequency=None, left_node=None, right_node=None, print_char=None):
        self.char = char
        self.frequency = frequency
        self.left_node = left_node
        self.right_node = right_node
        self.print_char = print_char

    def __repr__(self):
        return ''.join([self.char or '', str(self.frequency), str(self.left_node or '-'), str(self.right_node or '-')])

    @property
    def visible_char(self):
        return self.char or self.print_char or '???'

    def print(self):
        """Print nodes table."""
        left_char = self.left_node.visible_char if self.left_node else '-'
        right_char = self.right_node.visible_char if self.right_node else '-'
        print('\t'.join([self.visible_char, str(self.frequency), left_char, right_char]))
        if self.left_node:
            self.left_node.print()
        if self.right_node:
            self.right_node.print()

    def __gt__(self, other):
        if not isinstance(other, HuffmanNode):
            return super(HuffmanNode, self).__gt__(other)
        return self.frequency < other.frequency


def pop_two_nodes(nodes):
    if len(nodes) > 1:
        #first=nodes.pop(0)
        #second=nodes.pop(0)
        return nodes.pop(0), nodes.pop(0)
    else:
        #print "[popFirstTwoNodes] nodes's length <= 1"
        return nodes[0], None


def _build_tree(nodes):
    nodes.sort()
    index = 0
    while(True):
        first, second = pop_two_nodes(nodes)
        if not second:
            return first
        parent = HuffmanNode(
            left_node=first,
            right_node=second,
            frequency=first.frequency + second.frequency,
            print_char="M{}".format(index)
        )
        index += 1
        # first.p = parent
        # second.p = parent
        nodes.insert(0, parent)
        nodes.sort()


def _cal_freq(long_str):
    d = defaultdict(int)
    for c in long_str:
        d[c] += 1
    return d


def _gen_huffman_code(node, dict_codes, buffer_stack=[]):
    if not node.left_node and not node.right_node:
        dict_codes[node.char] = ''.join(buffer_stack)
        return
    buffer_stack.append('0')
    _gen_huffman_code(node.left_node, dict_codes, buffer_stack)
    buffer_stack.pop()

    buffer_stack.append('1')
    _gen_huffman_code(node.right_node, dict_codes, buffer_stack)
    buffer_stack.pop()


MAX_BITS = 8


class Encoder(object):
    def __init__(self, filename_or_long_str=None, mode=None):
        self.long_str = 'Samotoy'
        if filename_or_long_str:
            if os.path.exists(filename_or_long_str):
                self.encode(filename_or_long_str)
            else:
                print '[Encoder] take \'%s\' as a string to be encoded.'\
                      % filename_or_long_str
                self.long_str = filename_or_long_str

    def __get_long_str(self):
        return self._long_str

    def __set_long_str(self, s):
        self._long_str = s
        if s:
            self.root = self._get_tree_root()
            self.code_map = self._get_code_map()
            self.array_codes, self.code_length = self._encode_as_bytes()
    long_str = property(__get_long_str, __set_long_str)

    def _get_tree_root(self):
        d = _cal_freq(self.long_str)
        return _build_tree(
            [HuffmanNode(char=char, frequency=int(frequency)) for char, frequency in d.items()]
            )

    def _get_code_map(self):
        a_dict = {}
        _gen_huffman_code(self.root, a_dict)
        return a_dict

    def _encode_as_bytes(self):
        array_codes = array.array('B')
        code_length, buff, length = 0, 0, 0
        for ch in self.long_str:
            code = self.code_map[ch]
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

        if length != 0:
            array_codes.extend([buff << (MAX_BITS - length)])

        return array_codes, code_length

    def _encode_as_string(self):
        encoded_string = ''
        for ch in self.long_str:
            encoded_string += self.code_map[ch]
        return encoded_string, len(encoded_string)

    def encode(self, filename):
        fp = open(filename, 'rb')
        self.long_str = fp.read()
        fp.close()

    def write(self, filename):
        if self._long_str:
            fcompressed = open(filename, 'wb')
            marshal.dump(
                (pickle.dumps(self.root), self.code_length, self.array_codes),
                fcompressed)
            fcompressed = open(filename + '2', 'wb')
            pickle.dump(
                (pickle.dumps(self.root), self.code_length, self.array_codes),
                fcompressed)
            fcompressed.close()
        else:
            print("Please set long_str.")


class Decoder(object):
    def __init__(self, filename_or_raw_str=None):
        if filename_or_raw_str:
            if os.path.exists(filename_or_raw_str):
                filename = filename_or_raw_str
                self.read(filename)
            else:
                print('[Decoder] take \'%s\' as raw string' % filename_or_raw_str)
                raw_string = filename_or_raw_str
                unpickled_root, length, array_codes = marshal.loads(raw_string)
                self.root = pickle.loads(unpickled_root)
                self.code_length = length
                self.array_codes = array.array('B', array_codes)

    def _decode(self):
        string_buf = []
        total_length = 0
        node = self.root
        for code in self.array_codes:
            buf_length = 0
            while (buf_length < MAX_BITS and total_length != self.code_length):
                buf_length += 1
                total_length += 1
                if code >> (MAX_BITS - buf_length) & 1:
                    node = node.right_node
                    if node.char:
                        string_buf.append(node.char)
                        node = self.root
                else:
                    node = node.left_node
                    if node.char:
                        string_buf.append(node.char)
                        node = self.root

        return ''.join(string_buf)

    def read(self, filename):
        fp = open(filename, 'rb')
        unpickled_root, length, array_codes = marshal.load(fp)
        self.root = pickle.loads(unpickled_root)
        self.code_length = length
        self.array_codes = array.array('B', array_codes)
        fp.close()

    def decode_as(self, filename):
        decoded = self._decode()
        fout = open(filename, 'w')
        fout.write(decoded)
        fout.close()


enc = Encoder()
enc.root.print()
enc.write('test.txt')
dec = Decoder('test.txt')
dec.root.print()
dec.decode_as('test2.txt')
