class exceptions(Exception):

    def __init__(self, text: str = ''):
        super().__init__(text)


class argument_exception(exceptions):
    '''
    Ошибка передачи аргументов. Несоответсвие типов. Несоответсвие условиям.
    '''
    pass


class operation_exception(exceptions):
    '''
    Ошибка выполнения определённой операции.
    '''
    pass