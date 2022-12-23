import re
from typing import Tuple
from enum import Enum


class Lexems(Enum):
    BEGIN_OBJECT = '{'
    END_OBJECT = '}'
    BEGIN_ARRAY = '['
    END_ARRAY = ']'
    COMMA = ','
    COLON = ':'

    @classmethod
    def has_key(cls, item):
        return any(x for x in cls if x.value == item)


def solve_string(string: str) -> Tuple[str, str]:

    # заводим переменную для вывода
    output = ''

    # создаём цикл для чтения файла(условие окончания двойная кавычка)
    while string[0] != '"':

        # мы нашли защищённый файл?
        if string[0] == '\\' and string[1] == '"':
            # если да

            # добавляем их в вывод
            output += "\""

            # удалим из читаемого файла
            string = string[2:]
            continue
            # добавляем символ в вывод
        output += string[0]

        # удаляем символ из читаемого файла
        string = string[1:]

    # возвращаем читаемый файл
    return output, string[1:]


def json_analyzer(file_name: str):

    # читаем файл
    with open(file_name, mode='r', encoding='UTF-8') as f:
        data = f.read()

    # Начинаем вывод красиво :)
    print('Token list:')

    # создаём счётчик линий для возможных ошибок
    line_no = 1

    #Пуста ли data?
    while data:
    #data не пуста

        if data[0] == '\n':
            line_no += 1
            data = data[1:]
            continue

        elif data[0] == ' ':
            data = data[1:]
            continue

        # лексема из одного символа
        elif Lexems.has_key(data[0]):
            lexem = Lexems(data[0])
            print(f"({lexem.name}, ‘{lexem.value}’)")
            data = data[1:]

        # правда
        elif data.startswith('true'):
            print("(LITERAL, ‘true’)")
            data = data[4:]

        # ложь
        elif data.startswith('false'):
            print("(LITERAL, ‘false’)")
            data = data[5:]

        # пустышка
        elif data.startswith('null'):
            print("(LITERAL, ‘null’)")
            data = data[4:]

        # проверяем наличие читаемого файла
        elif data[0] == '"':

            # удаляем начальную двойные кавычки
            data = data[1:]

            # заносим читаемый файл в функцию
            string, data = solve_string(data)

            # выводим его
            print(f'(STRING, ‘{string}’)')

        elif data[0].isdigit() or data[0] == '-' or data[0] == '+':
            for string in re.finditer('-?[0-9]+.?e?\d+', data):
                string = string.group(0)
                break
            else:
                raise RuntimeWarning(f"Can't understand number at line {line_no}")
            data = data[len(string):]


            print(f'(NUMBER, {string})')

        # находим неизвестные символы
        else:
            raise RuntimeWarning(f'Unknown character "{data[0]}" at {line_no}')


def main():
    json_analyzer('data.json')


if __name__ == '__main__':
    main()
