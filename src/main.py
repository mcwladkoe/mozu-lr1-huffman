
import sys

from .encoder import Encoder
from .decoder import Decoder


def main():
    while True:
        print("""
            --- МЕНЮ ---
            0 - ввести строку с клавиатуры
            1 - выбрать файл
            2 - использовать фамилию студента
            3 - выход из программы
        """)
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
                break
        print("""
            --- МЕНЮ ---
            0 - хранить как битовый массив(array)
            1 - хранить как строку
            2 - выход в предыдущее меню
        """)
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
                print("""
                    --- МЕНЮ ---
                    0 - pickle + pickle
                    1 - pickle + marshal
                    2 - выход в предыдущее меню
                """)
                while True:
                    try:
                        menu2 = int(input("Выберите режим сериализации: "))
                    except ValueError:
                        print("Неверный мод")
                        continue
                    if menu2 not in range(3):
                        print("Неверный мод")
                    elif menu2 == 2:
                        break
                    else:
                        pass
    sys.exit()
    enc = Encoder('raw.txt')
    enc.write('test.txt')
    dec = Decoder('test.txt')
    dec.decode_as('test2.txt')


if __name__ == '__main__':
    main()
