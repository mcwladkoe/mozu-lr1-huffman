
import sys

from .encoder import Encoder
from .decoder import Decoder
from .menu_strings import *


def main():
    long_str = None
    filename = None
    while True:
        print(menu1_string)
        while True:
            try:
                menu1 = int(input("Выберите режим работы: "))
            except ValueError:
                print("Неверный мод")
                continue
            if menu1 not in range(4):
                print("Неверный мод")
            elif menu1 == 3:
                sys.exit(0)
            else:
                if menu1 == 2:
                    long_str = 'Самотой'
                elif menu1 == 0:
                    long_str = input("Введите строку: ")
                elif menu1 == 1:
                    # filename = 'world95.txt'
                    filename = '101.EXE'
                    # filename = input("Введите имя файла: ")
                break
        print(menu2_string)
        while True:
            try:
                menu2 = int(input("Выберите режим хранения: "))
            except ValueError:
                print("Неверный мод")
                continue
            if menu2 not in range(3):
                print("Неверный мод")
            elif menu2 == 2:
                break
            else:
                print(menu3_string)
                while True:
                    try:
                        menu3 = int(input("Выберите режим сериализации: "))
                    except ValueError:
                        print("Неверный мод")
                        continue
                    if menu3 not in range(4):
                        print("Неверный мод")
                    elif menu3 == 3:
                        break
                    else:
                        enc = Encoder(
                            filename=filename,
                            encode_mode=menu2,
                            serialize_mode=menu3,
                            long_str=long_str
                        )
                        out_filename = '{}_encoded.mcwladkoe'.format(filename or 'temp')
                        enc.write(out_filename)
                        dec = Decoder(
                            filename=out_filename,
                            encode_mode=menu2,
                            serialize_mode=menu3
                        )
                        out2_filename = '{}_decoded.mcwladkoe'.format(filename or 'temp')
                        dec.decode_as(out2_filename)
                        break
    sys.exit()


if __name__ == '__main__':
    main()
