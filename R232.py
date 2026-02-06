class parram:
    def __init__(self):
        self.mem_len = 0xffffff
        self.max_number = 0xffffffff
        self.width = 32
        self.insruction_len = 2
        self.order = 'big-endian'

        self.REGISTERS = {
            'zero': 0, 'pc1': 15, 'pc2': 14, 'ap1': 12, 'ap':12, 'tmp': 10, '$0': 0, '$1': 1, '$2': 2, '$3': 3, '$4': 4,
            '$5': 5, '$6': 6,
            '$7': 7, '$8': 8, '$9': 9, '$10': 10, '$11': 11, 'time': 11, '$12': 12, '$13': 13, '$14': 14, '$15': 15,
            'zp': 14,
            #EXTEND REG
            "r0" : 4,
            "r1" : 5,
            "r2" : 6,
            "r3" : 7,
            "r4" : 8,
            "r5" : 9,
            "r6" : 10,
            "r7" : 11,
            "r8" : 12,
            "r9" : 13,
            "r10" : 14,
            "r11" : 15,
            "r12" : 16,
            "r13" : 17,
            "r14" : 18,
            "r15" : 19,
            "r16" : 20,
            "r17" : 21,
            "r18" : 22,
            "r19" : 23,
            "r20" : 24,
            "r21" : 25,
            "r22" : 26,
            "r23" : 27,
            "r24" : 28,
            "r25" : 29,
            "r26" : 30,
            "r27" : 31,
            "r28" : 32,
        }
        self.COMMANDS = {
            # Специальные команды
            'DATA=': 'spec',
            '#define': 'spec',
            'fn:': 'spec',
            ':': 'spec',

            'nope' : '0 + 0',
            'cpuInfo': '0x1a+0',
            'push': "0x16 + 0",
            'return': '0x17 + 0',
            'ret_intr': '0x18+0',
            'stop': '0x18+0',
            'j': '0x14+0',

            'word': "number_string(arg1) + (number_string(arg1)<<32)",
            'jmp': "0x54 + (get_label(arg1)<<32)",
            'cpuInfo_0x': "0x5a + (number_string(arg1)<<32)",
            'beqAP': "0x10 + RS0(get_register(arg1)) + RS1(get_register(arg2))",
            'blqAP': "0x12 + RS0(get_register(arg1)) + RS1(get_register(arg2))",
            'bgqAP': "0x13 + RS0(get_register(arg1)) + RS1(get_register(arg2))",
            'beq': "0x50 + RS0(get_register(arg1)) + RS1(get_register(arg2)) + (get_label(arg3)<<32)",
            'bgq': "0x52 + RS0(get_register(arg1)) + RS1(get_register(arg2)) + (get_label(arg3)<<32)",
            'blq': "0x53 + RS0(get_register(arg1)) + RS1(get_register(arg2)) + (get_label(arg3)<<32)",
            'j_0x': "0x54 + (number_string(arg1)<<32)",
            'mel':"0x5 + ARG(get_register(arg1))",
            'ms': "0x6 + ARG(get_register(arg1))",
            'mel0x': "0x45 + ARG(get_register(arg2)) + (number_string(arg1)<<32)",
            'ms0x': "0x46 + ARG(get_register(arg2)) + (number_string(arg1)<<32)",
            'sb': "1 + RS0(get_register(arg1)) + (number_string(arg2)<<32)",
            'mov': '0x48 + RS0(get_register(arg2)) + RS1(get_register(arg1))',
            'cr' : "0x46 + (0xffffffff<<32)",

            'add': '0x08 + RS0(get_register(arg1)) + RS1(get_register(arg2)) + RS2(get_register(arg3))',
            'addi': '0x48 + RS0(get_register(arg1)) + RS1(get_register(arg2)) + (number_string(arg3)<<32)',
            'sub': '0x09 + RS0(get_register(arg1)) + RS1(get_register(arg2)) + RS2(get_register(arg3))',
            'subi': '0x49 + RS0(get_register(arg1)) + RS1(get_register(arg2)) + (number_string(arg3)<<32)',
            'and': '0x0C + RS0(get_register(arg1)) + RS1(get_register(arg2)) + RS2(get_register(arg3))',
            'andi': '0x4C + RS0(get_register(arg1)) + RS1(get_register(arg2)) + (number_string(arg3)<<32)',
            'xor': '0x0D + RS0(get_register(arg1)) + RS1(get_register(arg2)) + RS2(get_register(arg3))',
            'xori': '0x4D + RS0(get_register(arg1)) + RS1(get_register(arg2)) + (number_string(arg3)<<32)',
            'ror': '0x0E + RS0(get_register(arg1)) + RS1(get_register(arg2)) + RS2(get_register(arg3))',
            'rori': '0x4E + RS0(get_register(arg1)) + RS1(get_register(arg2)) + (number_string(arg3)<<32)',
            'rol': '0x0F + RS0(get_register(arg1)) + RS1(get_register(arg2)) + RS2(get_register(arg3))',
            'roli': '0x4F + RS0(get_register(arg1)) + RS1(get_register(arg2)) + (number_string(arg3)<<32)',

            #EX

            'mul' : "0x1 + RS0(10) + ((0+ERS0(get_register(arg1))) + ERS1(get_register(arg2)) + ERS2(get_register(arg3))<<32)"
                    "+ ((0x46 + ARG(10))<<64) + (0x21 << 96)",
            'div' : "0x1 + RS0(10) + ((1+ERS0(get_register(arg1))) + ERS1(get_register(arg2)) + ERS2(get_register(arg3))<<32)"
                    "+ ((0x46 + ARG(10))<<64) + (0x21 << 96)",
            'fadd' : "0x1 + RS0(10) + ((2+ERS0(get_register(arg1))) + ERS1(get_register(arg2)) + ERS2(get_register(arg3))<<32)"
                    "+ ((0x46 + ARG(10))<<64) + (0x21 << 96)",
            'fsub' : "0x1 + RS0(10) + ((3+ERS0(get_register(arg1))) + ERS1(get_register(arg2)) + ERS2(get_register(arg3))<<32)"
                    "+ ((0x46 + ARG(10))<<64) + (0x21 << 96)",
            'fmul' : "0x1 + RS0(10) + ((4+ERS0(get_register(arg1))) + ERS1(get_register(arg2)) + ERS2(get_register(arg3))<<32)"
                    "+ ((0x46 + ARG(10))<<64) + (0x21 << 96)",
            'fdiv' : "0x1 + RS0(10) + ((5+ERS0(get_register(arg1))) + ERS1(get_register(arg2)) + ERS2(get_register(arg3))<<32)"
                    "+ ((0x46 + ARG(10))<<64) + (0x21 << 96)",
            'sqrt' : "0x1 + RS0(10) + ((6+ERS0(get_register(arg1))) + ERS1(get_register(arg2))<<32)"
                    "+ ((0x46 + ARG(10))<<64) + (0x21 << 96)",
            'fmod' : "0x1 + RS0(10) + ((7+ERS0(get_register(arg1))) + ERS1(get_register(arg2)) + ERS2(get_register(arg3))<<32)"
                    "+ ((0x46 + ARG(10))<<64) + (0x21 << 96)",
            'fpow' : "0x1 + RS0(10) + ((8+ERS0(get_register(arg1))) + ERS1(get_register(arg2)) + ERS2(get_register(arg3))<<32)"
                    "+ ((0x46 + ARG(10))<<64) + (0x21 << 96)",
            'sin' : "0x1 + RS0(10) + ((9+ERS0(get_register(arg1))) + ERS1(get_register(arg2))<<32)"
                    "+ ((0x46 + ARG(10))<<64) + (0x21 << 96)",
            'cos' : "0x1 + RS0(10) + ((10+ERS0(get_register(arg1))) + ERS1(get_register(arg2))<<32)"
                    "+ ((0x46 + ARG(10))<<64) + (0x21 << 96)",
            'tg' : "0x1 + RS0(10) + ((11+ERS0(get_register(arg1))) + ERS1(get_register(arg2))<<32)"
                    "+ ((0x46 + ARG(10))<<64) + (0x21 << 96)",
            'eq' : "0x1 + RS0(10) + ((12+ERS0(get_register(arg1))) + ERS1(get_register(arg2)) + ERS2(get_register(arg3))<<32)"
                    "+ ((0x46 + ARG(10))<<64) + (0x21 << 96)",
            'lq' : "0x1 + RS0(10) + ((13+ERS0(get_register(arg1))) + ERS1(get_register(arg2)) + ERS2(get_register(arg3))<<32)"
                    "+ ((0x46 + ARG(10))<<64) + (0x21 << 96)",
            'gq' : "0x1 + RS0(10) + ((14+ERS0(get_register(arg1))) + ERS1(get_register(arg2)) + ERS2(get_register(arg3))<<32)"
                    "+ ((0x46 + ARG(10))<<64) + (0x21 << 96)",
            'itf' : "0x1 + RS0(10) + ((15+ERS0(get_register(arg1))) + ERS1(get_register(arg2))<<32)"
                    "+ ((0x46 + ARG(10))<<64) + (0x21 << 96)",
            'frnd' : "0x1 + RS0(10) + ((16+ERS0(get_register(arg1))) + ERS1(get_register(arg2))<<32)"
                    "+ ((0x46 + ARG(10))<<64) + (0x21 << 96)",
            
            'fmv.w.x' : "0x46 + ARG(get_register(arg1)) + ((get_register(arg2))<<32)",
            'fmv.x.w' : "0x45 + ARG(get_register(arg2)) + ((get_register(arg1))<<32)",
            
        }  # сюда кодирование

        self.LEN = {
                    "DATA=" : 1,
                    "#define" : 1,
                    "fn:" : 1,
                    ":" : 1,
                    "cpuInfo" : 1,
                    "push" : 1,
                    "return" : 1,
                    "ret_intr" : 1,
                    "stop" : 1,
                    "j" : 1,
                    "word" : 1,
                    "jmp" : 1,
                    "cpuInfo_0x" : 1,
                    "beqAP" : 1,
                    "blqAP" : 1,
                    "bgqAP" : 1,
                    "beq" : 1,
                    "bgq" : 1,
                    "blq" : 1,
                    "j_0x" : 1,
                    "mel" : 1,
                    "ms" : 1,
                    "mel0x" : 1,
                    "ms0x" : 1,
                    "sb" : 1,
                    "mov" : 1,
                    "cr" : 1,
                    "add" : 1,
                    "const_add" : 1,
                    "sub" : 1,
                    "const_sub" : 1,
                    "and" : 1,
                    "const_and" : 1,
                    "xor" : 1,
                    "const_xor" : 1,
                    "ror" : 1,
                    "const_ror" : 1,
                    "rol" : 1,
                    "const_rol" : 1,
                    "_mov" : 1,
                    'nope' : 1,
                    "mul" : 2,
                    "div" : 2,
                    "fadd" : 2,
                    "fsub" : 2,
                    "fmul" : 2,
                    "fdiv" : 2,
                    "sqrt" : 2,
                    "fmod" : 2,
                    "fpow" : 2,
                    "sin" : 2,
                    "cos" : 2,
                    "tg" : 2,
                    "eq" : 2,
                    "lq" : 2,
                    "gq" : 2,
                    "itf" : 2,
                    "frnd" : 2,

                    }

        self.functions = {
            'RS0' : self.RS0,
            'RS1' : self.RS1,
            'RS2' : self.RS2,
            'ARG' : self.AREG,
            'ERS0' : self.ERS0,
            'ERS1' : self.ERS1,
            'ERS2' : self.ERS2,
            'print' : print,
        }

        self.Labels = {
            'null' : 0,
            '0' : 0,
            #define's
            'HUB_MEM_ADRESS' : 0x100,
            'HUB_IO_ADRESS' : 0x101,

            "INTERRUPT_HANDLER_TABLE": 0x61,

            # Port B - Data Registers
            "PB0_DATA": 0x29,
            "PB1_DATA": 0x2B,
            "PB2_DATA": 0x2D,
            "PB3_DATA": 0x2F,
            "PB4_DATA": 0x31,
            "PB5_DATA": 0x33,
            "PB6_DATA": 0x35,
            "PB7_DATA": 0x37,

            # Port B - Mode Registers
            "PB0_MODE": 0x2a,
            "PB1_MODE": 0x26,
            "PB2_MODE": 0x2E,
            "PB3_MODE": 0x30,
            "PB4_MODE": 0x32,
            "PB5_MODE": 0x34,
            "PB6_MODE": 0x36,
            "PB7_MODE": 0x38,

            # GPIO Mode Definitions
            "GPIO_OUTPUT": 0x1,
            "GPIO_INTR": 0x2,
            "GPIO_BYTE_MODE_INPUT": 0x3,
            "GPIO_BYTE_MODE_OUTPUT": 0x4,
            "GPIO_TRIG": 0x5,

            # Interrupt Vector Addresses
            "INT_PB0": 0x49,
            "INT_PB1": 0x4a,
            "INT_PB2": 0x4b,
            "INT_PB3": 0x4c,
            "INT_PB4": 0x4d,
            "INT_PB5": 0x4e,
            "INT_PB6": 0x4f,
            "INT_PB7": 0x50,
        }


    def RS0(self, num):
        return num << 8

    def RS1(self, num):
        return num << 12

    def RS2(self, num):
        return num << 16

    def ERS0(self, num):
        return num<<8
    def ERS1(self, num):
        return num<<16
    def ERS2(self, num):
        return num<<24
    
    def AREG(self, num):
        return self.RS0(num) + self.RS1(num) + self.RS2(num)
