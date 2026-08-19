class parram:
    def __init__(self):

        self.name = "exemple"

        self.mem_len =      0xffffff # Объем адресного пространства (слов)
        self.max_number = 0xffffffff # Максимальное обрабатываемое число
        self.width =              32 # Разрядность слова
        self.insruction_len =      2 # Минимальная длинна инструкции (слов)
        self.order =    'big-endian' # Порядок слов в инструкции

        self.REGISTERS = {
# Регистр: Индекс
# Считается что в каждый регистр помещяеться ровно одно слово
            'zero': 0,
            'r0': 0,
        }

        self.COMMANDS = {
# TODO: ISA
# " Имя операции " : eval { кодирование }
            'jmp' : "0xFF + get_label(arg1) << 32 ", # ПРИМЕР
            # Встроенные
            'data=': 'spec',    # НЕ УДАЛЯТЬ
            '#define': 'spec',  # НЕ УДАЛЯТЬ
            'fn:': 'spec',      # НЕ УДАЛЯТЬ
            ':': 'spec',        # НЕ УДАЛЯТЬ

            "word" : "number_string(arg1) + (number_string(arg2) << 32)",
        }

        self.LEN = {            # Обязательно
# TODO: Количество машинных слов на инструкцию
            "data=" : 1,        # НЕ УДАЛЯТЬ
            "#define" : 1,      # НЕ УДАЛЯТЬ
            "fn:" : 1,          # НЕ УДАЛЯТЬ
            ":" : 1,            # НЕ УДАЛЯТЬ

            "word" : 1,
        }

        self.functions = {      # Обязательно
# TODO: Пользовательские функции указанные далее
            'RS0' : self.RS0,
        }

        self.Labels = {         # Обязательно
            # TODO: Метки
            'null' : 0,
        }

    def RS0(self, num):
        return num << 8
