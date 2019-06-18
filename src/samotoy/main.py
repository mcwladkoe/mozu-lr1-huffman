# NAME: Samotoy Vladyslav, 8.04.122.010.18.02.
import sys
import argparse

import os

from .encoder import Encoder
from .decoder import Decoder
from .menu_strings import menu1, menu2, menu3
from .serialize_modes import serialize_modes_extended, serialize_modes


class Main:
    """Main class."""

    def __init__(self, args=sys.argv, filename=None):
        """Initialize HuffmanNode object.

        Keyword arguments:
        args -- arguments object (default: sys.argv)
        """
        print(args)
        print(filename)
        self.long_str = None
        self.filename = None
        description = """\
            Huffman coding script
        """
        parser = argparse.ArgumentParser(description=description)
        parser.add_argument('--mode', metavar='mode',
            type=int,
            help='Режим работы\n{}'.format('\n'.join([
                '{} - {}'.format(k, v)
                for k, v in menu1.items()
            ])),
            choices=list(menu1)
        )
        parser.add_argument('--smode', metavar='smode',
            help='Режим хранения\n{}'.format('\n'.join([
                '{} - {}'.format(k, v)
                for k, v in menu2.items()
            ])),
            type=int,
            choices=list(menu2)
        )
        parser.add_argument('--file', metavar='file',
            help='Файл для кодирования',
        )
        parser.add_argument('--emode', metavar='emode',
            help='Режим режим сериализации\n{}'.format('\n'.join([
                '{} - {}'.format(k, v['description'])
                for k, v in menu3.items()
            ])),
            type=int,
            choices=list(menu3)
        )
        arg = parser.parse_args(args[1:])
        self.choise1 = arg.mode
        self.choise2 = arg.smode
        self.choise3 = arg.emode
        self.filename = filename or arg.file
        self.menu1()

    def menu1(self):
        """Menu step 1."""
        while not self.choise1:
            print('--- МЕНЮ ---')
            for key, val in menu1.items():
                print('{} - {}'.format(key, val))
            print('0 - выход из программы')
            try:
                self.choise1 = int(input("Выберите режим работы: "))
            except ValueError:
                print("Неверный мод")
                continue
            if self.choise1 not in menu1:
                print("Неверный мод")
            elif self.choise1 == 0:
                sys.exit(0)

        if self.choise1 == 2:
            self.long_str = 'Самотой'
        elif self.choise1 == 3:
            self.long_str = input("Введите строку: ")
        elif self.choise1 == 1 and not self.filename:
            self.filename = input("Введите имя файла: ")
        self.menu2()

    def menu2(self):
        """Menu step 2."""
        while not self.choise2:
            print('--- МЕНЮ ---')
            for key, val in menu2.items():
                print('{} - {}'.format(key, val))
            print('0 - выход в предыдущее меню')
            try:
                self.choise2 = int(input("Выберите режим хранения: "))
            except ValueError:
                print("Неверный мод")
                self.choise2 = None
                continue
            if self.choise2 not in menu2:
                print("Неверный мод")
                self.choise2 = None
            elif self.choise2 == 0:
                self.choise2 = None
                self.choise1 = None
                self.menu1()

        self.menu3()

    def menu3(self):
        """Menu step 3 + processing."""
        while not self.choise3:
            print('--- МЕНЮ ---')
            for key, val in menu3.items():
                print('{} - {}'.format(key, val['description']))
            print('0 - выход в предыдущее меню')
            try:
                self.choise3 = int(input("Выберите режим сериализации: "))
            except ValueError:
                print("Неверный мод")
                self.choise3 = None
                continue
            if self.choise3 not in serialize_modes_extended:
                print("Неверный мод")
                self.choise3 = None
            elif self.choise3 == 0:
                self.choise3 = None
                self.choise2 = None
                self.menu2()

        if self.choise3 == 100:
            for i in serialize_modes.keys():
                enc = Encoder(
                    filename=self.filename,
                    encode_mode=self.choise2,
                    serialize_mode=i,
                    long_str=self.long_str
                )
                out_filename = '{}_encoded_{}.mcwladkoe'.format(
                    self.filename or 'temp',
                    i
                )
                enc.write(out_filename)
                dec = Decoder(
                    filename=out_filename,
                    encode_mode=self.choise2,
                    serialize_mode=i
                )
                out2_filename = '{}_decoded_{}.mcwladkoe'.format(
                    self.filename or 'temp',
                    i
                )
                dec.decode_as(out2_filename)
        else:
            enc = Encoder(
                filename=self.filename,
                encode_mode=self.choise2,
                serialize_mode=self.choise3,
                long_str=self.long_str
            )
            out_filename = '{}_encoded.mcwladkoe'.format(
                self.filename or 'temp'
            )
            enc.write(out_filename)
            dec = Decoder(
                filename=out_filename,
                encode_mode=self.choise2,
                serialize_mode=self.choise3
            )
            out2_filename = '{}_decoded.mcwladkoe'.format(
                self.filename or 'temp'
            )
            dec.decode_as(out2_filename)
            self.choise3 = None
            self.choise2 = None
            self.choise1 = None
            self.menu1()


def main():
    # file = []
    # for root, _, files in os.walk("ТЕСТОВЫЕ ФАЙЛЫ", topdown=False):
    #     for name in files:
    #         file.append(os.path.join(os.path.join(root, name)))
    # for i in file:
    #     print(i)
    #     Main(filename=os.path.join('/home/vlads/Projects/mozu-lr1-huffman', i))
    Main()

if __name__ == '__main__':
    main()
