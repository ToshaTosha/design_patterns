
"""
Настройки
"""


class Settings:
    __inn = ""
    __account = ""
    __correspondent_account = ""
    __bik = ""
    __business_type = ""

    @property
    def inn(self):
        return self.__inn

    @inn.setter
    def inn(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Некорректно переданы параметры!")
        if len(value) != 12:
            raise ValueError("Номер ИНН должен быть 12 символов")

        self.__inn = value

    @property
    def account(self):
        return self.__account

    @account.setter
    def account(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Некорректно переданы параметры!")
        if len(value) != 11:
            raise ValueError("Номер счёта должен быть 11 символов")
        self.__account = value

    @property
    def correspondent_account(self):
        return self.__correspondent_account

    @correspondent_account.setter
    def correspondent_account(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Некорректно переданы параметры!")
        if len(value) != 11:
            raise ValueError("Корреспондентский счет должен быть 11 символов")
        self.__correspondent_account = value

    @property
    def bik(self):
        return self.__bik

    @bik.setter
    def bik(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Некорректно переданы параметры!")
        if len(value) != 9:
            raise ValueError("БИК должен быть 9 символов")
        self.__bik = value

    @property
    def business_type(self):
        return self.__business_type

    @business_type.setter
    def business_type(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Некорректно переданы параметры!")
        if len(value) != 5:
            raise ValueError("Вид собственности должен быть 5 символов")
        self.__business_type = value