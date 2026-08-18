class parram:
    def __init__(self):
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

""" =============================
Встроенные функции:
    get_label ( name )  
    number_string ( str )
    get_register ( name ) 
++++++++++++++++++++++++++++++++
Агрументы:
    arg1
    arg2
    arg3    
    arg4    
============================= """
            # Встроенные
            'DATA=': 'spec',    # НЕ УДАЛЯТЬ
            '#define': 'spec',  # НЕ УДАЛЯТЬ
            'fn:': 'spec',      # НЕ УДАЛЯТЬ
            ':': 'spec',        # НЕ УДАЛЯТЬ
        }

        self.LEN = {            # Обязательно
# TODO: Количество машинных слов на инструкцию
            "DATA=" : 1,        # НЕ УДАЛЯТЬ
            "#define" : 1,      # НЕ УДАЛЯТЬ
            "fn:" : 1,          # НЕ УДАЛЯТЬ
            ":" : 1,            # НЕ УДАЛЯТЬ
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
