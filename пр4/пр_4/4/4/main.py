#Для ввода
from typing import Union
# Для выхода
import sys
# нумерация
from enum import IntFlag, auto
# Regexp
import re


class WrongState(Exception):
    __slots__ = ('message',)

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

    def _construct_message(self):
        return f'Wrong state: {self.message}'


class States(IntFlag):
    S = auto()
    A = auto()
    B = auto()
    C = auto()
    I = auto()
    N = auto()
    L = auto()
    Z = auto()
    ERROR_STATE = auto()
    END_STATE = auto()


class Automate:
    __slots__ = ('__string', '__state')
    __STRING_LIMIT = 10000
    __L = r'a-zA-Z'  # a|b...y|z|A|B...|Y|Z
    __Z = r'\d'  # 1|...|9

    def __init__(self, string: str):
        self.__string: str = string

    def run(self) -> States:
        self.S(self.__string[:self.__STRING_LIMIT])
        return self.__state

    def get_state(self) -> States:
        return self.__state

    def S(self, inp: str):
        __state: States = States.S
        pattern = r'for\s\(([^\)]*);([^\)]*);([^\)]*);\)\sdo\s([^;]*);\s?(.*)'

        # Вывод решения
        value = re.match(pattern, inp)

        if value is None:
            raise WrongState(f"Can't resolve state S with string {inp}")

        print('(ID, "for")\n(DLM, "(")', flush=True)

        # Первая проверка
        if self.A(value[1]) is None:
            raise WrongState(f"Error during specification AAA in state S")
        print('(DEL, ";")', flush=True)
        if self.A(value[2]) is None:
            raise WrongState(f"Error during specification AAA in state S")
        print('(DEL, ";")', flush=True)
        if self.A(value[3]) is None:
            raise WrongState(f"Error during specification AAA in state S")
        print('(DLM, ";")', flush=True)

        # for (A; A; A;) do S;
        # for (A; A; A;) do A;
        if self.A(value[4]) is None and self.S(value[4]) is None:
            raise WrongState(f'Can\'t do "{value[4]}"')

        # for (A; A; A;) do A; S
        if value[5]:
            self.S(value[5])

        self.__state = States.END_STATE

    def A(self, inp: Union[str, None] = None):
        pattern = r'([^(:=)]*)(:=)(.*)'
        if (value := re.match(pattern, inp)) is not None:
            if self.I(value[1]) is None:
                raise WrongState(f'Error in I state during resolving {value[1]}')

            print('(ASGN, ":=")', flush=True)

            if self.B(value[3]) is None:
                raise WrongState(f'Error in B state during resolving {value[3]}')
            return inp[value.pos:value.endpos]
        else:
            raise WrongState("Can't resolve A")

    def B(self, inp: str) -> Union[str, None]:
        pattern = r'([^>=<]*)([>=<])(.*)'
        if (value := re.match(pattern, inp)) is not None:
            if self.C(value[1]) is None:
                raise WrongState(f"B state can't be solve ({inp})")

            print(f'(DLM, "{value[2]}")', flush=True)

            if self.C(value[3]) is None:
                raise WrongState(f"B state can't be solve ({inp})")
            return inp[value.pos:value.endpos]

    def C(self, inp: str) -> Union[str, None]:
        if (value := self.I(inp)) is not None:
            return value
        elif (value := self.N(inp)) is not None:
            return value
        else:
            return None

    def I(self, inp: str):
        pattern = f'[_{self.__L}][_0{self.__L}{self.__Z}]?'
        if (value := re.match(pattern, inp)) is not None:
            value = value.group(0)
            print(f'(ID, "{value}")', flush=True)
            return value

    def N(self, inp: str):
        pattern = r'[-+]?(\d*\.?\d*)([eE][-+]?\d*[flFL]?)?'
        if (value := re.match(pattern, inp)) is not None:
            value = inp[value.pos:value.endpos]
            print(f'(NM, "{value}")', flush=True)
            return value

    def L(self):
        return NotImplemented  # user __L set instead

    def Z(self):
        return NotImplemented  # use __Z set instead


if __name__ == '__main__':
    au = Automate("for (a:=345<0;wq:=1>13;sd:=123>s2;) do d:=_2<_2;")
    if au.run() == States.END_STATE:
        sys.exit(0)
    else:
        sys.exit(1)
