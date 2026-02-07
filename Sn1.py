class parram:
    def __init__(self):
        self.mem_len = 0xfff
        self.max_number = 0xff
        self.width = 8
        self.insruction_len = 4
        self.order = 'little-endian'

        self.REGISTERS = {
            'zero' : 0, 'x0' : 0, 'x1' : 1, 'x2' : 2, 'x3' : 3, 'x4' : 4,
            'eq' : 5, 'ap' : 6, 'gp' : 7, 'tgp' : 8, 'pc' : 9, 'pc2' : 10
        }
        self.COMMANDS = {
            # Специальные команды
            'DATA=': 'spec',
            '#define': 'spec',
            'fn:': 'spec',
            ':': 'spec',
            'sb': '0x01000000 + RS1(get_register(arg1))',
            'lb': '0x02000000 + RS1(get_register(arg1))',
            'sbi': '0x09000000 + RS1(get_register(arg1)) + (number_string(arg2))',
            'ilb': '0x0a000000 + RS1(get_register(arg1)) + (number_string(arg2))',
            'add': '0x03000000 + RS0(get_register(arg1)) + RS1(get_register(arg2)) + RS2(get_register(arg3)) + (number_string(arg4))',
            'sub': '0x04000000 + RS0(get_register(arg1)) + RS1(get_register(arg2)) + RS2(get_register(arg3)) + (number_string(arg4))',
            'eq': '0x05000000 + RS1(get_register(arg1)) + RS2(get_register(arg2)) + (number_string(arg3))',
            'nand': '0x06000000 + RS0(get_register(arg1)) + RS1(get_register(arg2)) + RS2(get_register(arg3)) + (number_string(arg4))',
            'j': '0x07000000 + get_label(arg1)',
            'ij' : '0x08000000 + get_label(arg1)',
        }
            #сюда кодирование

        self.functions = {
            'RS0' : self.RS0,
            'RS1' : self.RS1,
            'RS2' : self.RS2,
            'print' : print,
        }

        self.LEN = {
            "DATA=": 1,
            "#define": 1,
            "fn:": 1,
            ":": 1,
            "sb": 1,
            "lb": 1,
            "sbi": 1,
            "ilb": 1,
            "add": 1,
            "sub": 1,
            "eq": 1,
            "nand": 1,
            "j": 1,
            "ij": 1,

            
        }

        self.Labels = {
            'null': 0,
            '0': 0,
        }

    def RS0(self, num):
        return num << 28

    def RS1(self, num):
        return num << 16

    def RS2(self, num):
        return num << 20
