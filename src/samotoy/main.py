
import sys

from .encoder import Encoder
from .decoder import Decoder
from .menu_strings import *
from .serialize_modes import serialize_modes_extended, serialize_modes


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
                    filename = input("Введите имя файла: ")
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
            elif menu2 == 0:
                break
            else:
                print(menu3_string)
                while True:
                    try:
                        menu3 = int(input("Выберите режим сериализации: "))
                    except ValueError:
                        print("Неверный мод")
                        continue
                    if menu3 not in serialize_modes_extended.keys():
                        print("Неверный мод")
                    elif menu3 == 0:
                        break
                    elif menu3 == 100:
                        for i in serialize_modes.keys():
                            enc = Encoder(
                                filename=filename,
                                encode_mode=menu2,
                                serialize_mode=i,
                                long_str=long_str
                            )
                            out_filename = '{}_{}_encoded.mcwladkoe'.format(i, filename or 'temp')
                            enc.write(out_filename)
                            dec = Decoder(
                                filename=out_filename,
                                encode_mode=menu2,
                                serialize_mode=i
                            )
                            out2_filename = '{}_{}_decoded.mcwladkoe'.format(i, filename or 'temp')
                            dec.decode_as(out2_filename)
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
