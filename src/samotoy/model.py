# NAME: Samotoy Vladyslav, 8.04.122.010.18.02.
import json


class H:
    """HuffmanNode object simplified."""

    def __init__(
        self,
        char=None,
        frequency=None,
        left_node=None,
        right_node=None
    ):
        """
        Initialize HuffmanNode object.

        Keyword arguments:
        char -- character of node (default: None)
        frequency -- character of char in source array (default: None)
        left_node -- left node (default: None)
        right_node -- right node (default: None)
        """
        self.C = char
        self.F = frequency
        self.L = left_node
        self.R = right_node

    def __repr__(self):
        """Representation of HuffmanNode."""
        return ''.join([
            str(self.C or 0x00),
            str(self.F),
            str(self.L or 0x00),
            str(self.R or 0x00)
        ])

    def __gt__(self, other):
        """Greater than override.

        Keyword arguments:
        other -- other object to (required)
        """
        if not isinstance(other, H):
            return super(H, self).__gt__(other)
        return self.F > other.F

    def print_node(self):
        """Print nodes table."""
        left_char = self.L.visible_char if self.L else '-'
        right_char = self.R.visible_char if self.R else '-'
        print('\t'.join([
            self.visible_char,
            str(self.F),
            left_char,
            right_char
        ]))
        if self.L:
            self.L.print_node()
        if self.R:
            self.R.print_node()

    @property
    def visible_char(self):
        """Property for print."""
        return self.C or '???'


class HSerializer:
    """Serializer for HuffmanNode(H) class as list."""

    def __init__(self, serializer=None):
        """Initialize class.

        Keyword arguments:
        serializer -- secondary serializer class (default: None)
        """
        self.serializer = serializer or json

    def recursive_dumps(self, obj):
        """Recursive dumping object.

        Keyword arguments:
        obj -- object to serialize
        """
        if not obj:
            return None
        data = [obj.C, self.recursive_dumps(obj.R)]
        if obj.L:
            data.append(self.recursive_dumps(obj.L))
        return data

    def recursive_loads(self, obj):
        """Recursive loads object.

        Keyword arguments:
        obj -- object to deserialize
        """
        if not obj:
            return
        ob = H()
        ob.C = obj[0]
        ob.R = self.recursive_loads(obj[1])
        if len(obj) > 2:
            ob.L = self.recursive_loads(obj[2])
        return ob

    def loads(self, raw):
        """Load object.

        Keyword arguments:
        obj -- object to deserialize
        """
        obj = self.serializer.loads(raw)
        return self.recursive_loads(obj)

    def dumps(self, obj):
        """Dumping object.

        Keyword arguments:
        obj -- object to serialize
        """
        data = self.recursive_dumps(obj)
        return self.serializer.dumps(data)


# class HDictSerializer:
#     @classmethod
#     def recursive_dumps(cls, obj):
#         data = {
#             'C': obj.C
#         }
#         if obj.R:
#             data['R'] = cls.recursive_dumps(obj.R)
#         if obj.L:
#             data['L'] = cls.recursive_dumps(obj.L)
#         return data

#     @classmethod
#     def dumps(cls, obj):
#         data = cls.recursive_dumps(obj)
#         return json.dumps(data)


# class HFullSerializer:
#     @classmethod
#     def recursive_dumps(cls, obj):
#         data = {
#             'C': obj.C
#         }
#         if obj.R:
#             data['R'] = cls.recursive_dumps(obj.R)
#         if obj.L:
#             data['L'] = cls.recursive_dumps(obj.L)
#         return data

#     @classmethod
#     def dumps(cls, obj):
#         data = recursive_dumps(obj)
#         return json.dumps(data)


class HuffmanNode:
    """HuffmanNode object."""

    def __init__(
        self,
        char=None,
        frequency=None,
        left_node=None,
        right_node=None,
        print_char=None
    ):
        """
        Initialize HuffmanNode object.

        Keyword arguments:
        char -- character of node (default: None)
        frequency -- character of char in source array (default: None)
        left_node -- left node (default: None)
        right_node -- right node (default: None)
        print_char -- visible chat(for print) (default: None)
        """
        self.char = char
        self.frequency = frequency
        self.left_node = left_node
        self.right_node = right_node
        self.print_char = print_char

    def __repr__(self):
        """Representation of HuffmanNode."""
        return ''.join([
            self.char or '',
            str(self.frequency),
            str(self.left_node or '-'),
            str(self.right_node or '-')
        ])

    @property
    def visible_char(self):
        """Property for print."""
        return self.char or self.print_char or '???'

    def print_node(self):
        """Print nodes table."""
        left_char = self.left_node.visible_char if self.left_node else '-'
        right_char = self.right_node.visible_char if self.right_node else '-'
        print('\t'.join([
            self.visible_char,
            str(self.frequency),
            left_char,
            right_char
        ]))
        if self.left_node:
            self.left_node.print_node()
        if self.right_node:
            self.right_node.print_node()

    def __gt__(self, other):
        """Greater than override.

        Keyword arguments:
        other -- other object to (required)
        """
        if not isinstance(other, HuffmanNode):
            return super(HuffmanNode, self).__gt__(other)
        return self.frequency < other.frequency
