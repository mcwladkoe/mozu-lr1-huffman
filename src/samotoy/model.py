import json


class H:
    def __init__(self, char=None, frequency=None, left_node=None, right_node=None, print_char=None):
        self.C = char
        self.F = frequency
        self.L = left_node
        self.R = right_node

    def __repr__(self):
        return ''.join([str(self.C or 0x00), str(self.F), str(self.L or 0x00), str(self.R or 0x00)])

    def __gt__(self, other):
        if not isinstance(other, H):
            return super(H, self).__gt__(other)
        return self.F > other.F

    def print(self):
        """Print nodes table."""
        left_char = self.L.visible_char if self.L else '-'
        right_char = self.R.visible_char if self.R else '-'
        print('\t'.join([self.visible_char, str(self.F), left_char, right_char]))
        if self.L:
            self.L.print()
        if self.R:
            self.R.print()

    @property
    def visible_char(self):
        return self.C or '???'


class HSerializer:
    def __init__(self, serializer=None):
        self.serializer = serializer or json

    def recursive_dumps(self, obj):
        if not obj:
            return None
        data = [obj.C, self.recursive_dumps(obj.R)]
        if obj.L:
            data.append(self.recursive_dumps(obj.L))
        return data

    def recursive_loads(self, obj):
        if not obj:
            return
        ob = H()
        ob.C = obj[0]
        ob.R = self.recursive_loads(obj[1])
        if len(obj) > 2:
            ob.L = self.recursive_loads(obj[2])
        return ob

    def loads(self, raw):
        obj = self.serializer.loads(raw)
        return self.recursive_loads(obj)

    def dumps(self, obj):
        data = self.recursive_dumps(obj)
        return self.serializer.dumps(data)


class HDictSerializer:
    @classmethod
    def recursive_dumps(cls, obj):
        data = {
            'C': obj.C
        }
        if obj.R:
            data['R'] = cls.recursive_dumps(obj.R)
        if obj.L:
            data['L'] = cls.recursive_dumps(obj.L)
        return data

    @classmethod
    def dumps(cls, obj):
        data = cls.recursive_dumps(obj)
        return json.dumps(data)


class HFullSerializer:
    @classmethod
    def recursive_dumps(cls, obj):
        data = {
            'C': obj.C
        }
        if obj.R:
            data['R'] = cls.recursive_dumps(obj.R)
        if obj.L:
            data['L'] = cls.recursive_dumps(obj.L)
        return data

    @classmethod
    def dumps(cls, obj):
        data = recursive_dumps(obj)
        return json.dumps(data)


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
