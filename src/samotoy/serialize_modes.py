import marshal
import pickle
from .model import HSerializer

serialize_modes = {
    1: {
        'description': 'pickle + pickle',
        'lib2': pickle,
        'lib1': pickle,
    },
    2: {
        'description': 'pickle + marshal',
        'lib2': marshal,
        'lib1': pickle,
    },
    30: {
        'description': 'self-made(json) + marshal',
        'lib2': marshal,
        'lib1': HSerializer(),
    },
    31: {
        'description': 'self-made(marshal) + marshal',
        'lib2': marshal,
        'lib1': HSerializer(marshal),
    },
    32: {
        'description': 'self-made(pickle) + marshal',
        'lib2': marshal,
        'lib1': HSerializer(pickle),

    },
    40: {
        'description': 'self-made(json) + pickle',
        'lib2': pickle,
        'lib1': HSerializer(),
    },
    41: {
        'description': 'self-made(marshal) + pickle',
        'lib2': pickle,
        'lib1': HSerializer(marshal),
    },
    42: {
        'description': 'self-made(pickle) + pickle',
        'lib2': pickle,
        'lib1': HSerializer(pickle),
    },
}

serialize_modes_extended = serialize_modes.copy()
serialize_modes_extended[100] = {
    'description': 'Все режимы'
}
