from .serialize_modes import serialize_modes_extended

menu1_string = """
--- МЕНЮ ---
0 - ввести строку с клавиатуры
1 - выбрать файл
2 - использовать фамилию студента
3 - выход из программы
"""

menu2_string = """
--- МЕНЮ ---
1 - хранить как битовый массив(array)
2 - хранить как строку
0 - выход в предыдущее меню
"""

menu3_string = """
--- МЕНЮ ---
"""
for key, val in serialize_modes_extended.items():
    menu3_string += '{} - {}\n'.format(key, val)
menu3_string += """0 - выход в предыдущее меню
"""
