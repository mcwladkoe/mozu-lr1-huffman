# NAME: Samotoy Vladyslav, 8.04.122.010.18.02.
from collections import defaultdict
from .model import H
MAX_BITS = 8


def pop_two_nodes(nodes):
    if len(nodes) > 1:
        f = nodes.pop(0)
        s = nodes.pop(0)
        return f, s
    else:
        return nodes[0], None


def build_tree(nodes):
    nodes.sort()
    index = 0
    while(True):
        first, second = pop_two_nodes(nodes)
        if not second:
            return first
        parent = H(
            left_node=first,
            right_node=second,
            frequency=first.F + second.F,
        )
        index += 1
        nodes.insert(0, parent)
        nodes.sort()


def get_frequency_table(long_str):
    ftable = defaultdict(int)
    for c in long_str:
        ftable[c] += 1
    return ftable


def generate_huffman_code(node, dict_codes, tmp=None):
    if not node.L and not node.R:
        dict_codes[node.C] = ''.join(tmp or '')
        return
    tmp = tmp or []
    tmp.append('0')
    generate_huffman_code(node.L, dict_codes, tmp)
    tmp.pop()

    tmp.append('1')
    generate_huffman_code(node.R, dict_codes, tmp)
    tmp.pop()
