class BaseException(Exception):
    pass


class ArgumentTypeException(BaseException):
    def __init__(self, arg: str, type: str):
        self.__message = f"Ожидается тип {type} для переменной {arg}"
        return super().__init__(self.__message)


class ArgumentMaxLengthException(BaseException):
    def __init__(self, arg: str, length: int):
        self.__message = f"Строка {arg} не должна превышать {length} символов"
        return super().__init__(self.__message)


class ArgumentLengthException(BaseException):
    def __init__(self, arg: str, length: int):
        self.__message = f"Строка {arg} должна быть равна {length} символов"
        return super().__init__(self.__message)


class EmptyException(BaseException):
    def __init__(self):
        self.__message = f"Данные отсутствуют!"
        return super().__init__(self.__message)


class UnknownValueException(BaseException):
    def __init__(self):
        self.__message = f"Неизвестные данные!"
        return super().__init__(self.__message)