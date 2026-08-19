from simpleeval import simple_eval
import time
import struct


class console():
    def __init__(self,command=None):
        self.command = command
        self.lines = []

    def print(self,str,end='\n',start=''):
        if start == '\r':
            if len(self.lines) > 0:
                self.lines.pop(-1)
            self.lines.append(f'{str}{end}')

        else:
            self.lines.append(f'{str}{start}')
        self.command(''.join(self.lines))

class compiler():

    def progressbar(self,proc):
        out = ''
        count = round(proc // 5)
        for i in range(count):
            out = out + '█'
        for i in range(19 - count):
            out = out + '░'
        self.con.print(f'Процесс компиляции 〚{out}〛{round(proc)}%', end='\n',start='\r')

    @staticmethod
    def to_hex(s):
        return hex(int(s)).replace('0x', '')

    @staticmethod
    def isnumber(num):
        flag = True
        for i in str(num):
            if i not in "-xboXBO0123456789aAbBcCdDeEfF":
                flag = False
        return flag

    @staticmethod
    def get_ind(list,ind):
        if len(list) - 1 >= ind:
            return list[ind]
        else:
            return 0

    def __init__(self,raw,sourse,format='Logisim',console_command = None):


        self.con = console(command=console_command)
        self._eval_cache = {}
        self.raw = raw.split('\n')
        self.lineN = 0
        self.line = self.raw[self.lineN]

        self.format = format

        self.arg1,self.arg2,self.arg3 = 1,0,0
        self.convert_flag = False
        self.out = []
        self.bin = bin

        self.mem = sourse.mem_len
        self.max_number = sourse.max_number
        self.width = sourse.width
        self.insruction_len = sourse.insruction_len
        self.order = sourse.order

        self.functions = {
            # default asm functions for blueprint
            'get_label': self.get_label,
            'number_string': self.number_string,
            'isnumber': self.isnumber,
            'get_register': self.get_register,

            # Встроенные функции Python
            'int': int,
            'list': list,
            'range': range,
            'len': len,
            'sum': sum,
            'sorted': sorted,
            'min': min,
            'max': max,
            'str': str,
            'abs': abs,
            'round': round,
            'bool': bool,
            'float': float,
            'hex': hex,
            'bin': bin,
            'ord': ord,
            'chr': chr,
            'List': list,
            'Tuple': tuple,
            'Dict': dict,
            'Set': set,
        }
        self.functions = self.functions | sourse.functions

        self.REGISTERS = sourse.REGISTERS
        self.COMMANDS = sourse.COMMANDS
        self.LABELS = sourse.Labels
        self.LEN = sourse.LEN

        self.percent_of_line = 100 / len(self.raw)
        self.percent_to_complite = 0

    def get_len(self,cmm):
        if cmm in self.LEN:
            return self.LEN[cmm]
        else:
            self.con.print(f"Ошибка словоря длинны {cmm}")
            self.convert_flag = False
            return 0

    def output_memory(self,list): #добавить связку адрес-значение
        print(list)
        if self.order == 'big-endian':
            for i in range(len(list)):
                self.out.append((i+self.memADR,list[i]))
        if self.order == 'little-endian':
            for i in range(len(list)):
                # Берем элементы с конца, но адресуем с начала
                reverse_idx = len(list) - 1 - i
                print(i,reverse_idx)
                self.out.append((i + self.memADR, list[reverse_idx]))

    def string_bias_expr(self, s):
        operands = []
        operators = []
        valid_operators = "+-&|^<>"
        str = ""
        for char in s:
            if char in valid_operators:
                if str == "":
                    self.bad_expression_bias(s, "двойной знак")
                    return 0
                operands.append(self.number_string(str))
                str = ""
                operators.append(char)
            else:
                str += char
        operands.append(self.number_string(str))
        print(operators)
        print(operands)

        if len(operands) < 2:
            self.bad_expression_bias(s, "число не является выражением")
            return 0

        if len(operands) - len(operators) != 1:
            self.bad_expression_bias(s, "неправильные операторы")
            return 0
        tmp = operands[0]
        n = 0
        for i in range(len(operators)):
            n = operands[i + 1]
            if operators[i] == "+": tmp = tmp + n
            if operators[i] == "-": tmp = tmp - n
            if operators[i] == "&": tmp = tmp & n
            if operators[i] == "|": tmp = tmp | n
            if operators[i] == "^": tmp = tmp ^ n
            if operators[i] == ">": tmp = tmp >> n
            if operators[i] == "<": tmp = tmp << n
        return tmp


    def number_string(self, s): #Художественный фильм "С3,14здели преобразователь строка-число в форматах : 0x 0b 0o "" int
        s = str(s)
        if not self.convert_flag:
            return 0
        if not s:
            self.con.print(f'L{self.lineN}: {self.line}\n<---Пустая строка')
            self.convert_flag = False
            return 0

        if (s.startswith("'") and s.endswith("'")) or (s.startswith('"') and s.endswith('"')):
            if len(s) < 3:
                self.sys_invalid_literal(s)
                return 0
            char_value = s[1:-1]

            if len(char_value) == 1:
                return ord(char_value)
            else:
                self.con.print(f'L{self.lineN}: {self.line}\n<---Символьный литерал должен содержать ровно один символ: {s}')
                self.convert_flag = False
                return 0

        elif s.startswith("[") and s.endswith("]"):
            o = self.string_bias_expr(s.replace('[','').replace(']',''))
            if o <= self.max_number:
                return o
            else:
                self.value_ovrfl(o)
                return 0

        s_lower = s.lower()
        try:

            if s_lower.startswith(':'):
                #label
                o = self.get_label(s[1:])
                if o <= self.max_number:
                    print(f'L{self.lineN}:{o}')
                    return o
                else:
                    self.value_ovrfl(o)
                    return 0

            elif s_lower.startswith('0x'):
                # Шестнадцатеричное число
                o = int(s[2:], 16)
                if o <= self.max_number:
                    return o
                else:
                    self.value_ovrfl(o)
                    return 0
            elif s_lower.startswith('0b'):
                # Двоичное число
                o = int(s[2:], 2)
                if o <= self.max_number:
                    return o
                else:
                    self.value_ovrfl(o)
                    return 0
            elif s_lower.startswith('0o'):
                # Восьмеричное число
                o = int(s[2:], 8)
                if o <= self.max_number:
                    return o
                else:
                    self.value_ovrfl(o)
                    return 0

            elif s_lower.startswith(':'):
                o = self.get_label(s[1:])
                if o <= self.max_number:
                    return o
                else:
                    print(f'L{self.lineN}:{o}')
                    self.value_ovrfl(o)
                    return 0

            elif s.lower().startswith("f"):
                try:
                    f = float(s[1:])
                    o = struct.unpack('>I', struct.pack('>f', f))[0]
                    if o > self.max_number:
                        print(f'L{self.lineN}:{o}')
                        self.value_ovrfl(o)
                        return 0
                    return o
                except ValueError:
                    pass

            else:
                # Десятичное число (может быть отрицательным)
                o = int(s, 10)
                if o <= self.max_number:
                    return o
                else:
                    self.value_ovrfl(o)
                    return 0

        except ValueError as e:
            self.con.print(f'L{self.lineN}: {self.line}\n<---Ошибка преобразования {s}: {e}')
            self.convert_flag = False
            return 0

    def no_comma_error(self,arg):
        self.con.print(f'L{self.lineN}: {self.line}\n<---Неизвестная команда {arg}')
        self.convert_flag = False

    def no_label_error(self,arg):
        self.con.print(f'L{self.lineN}: {self.line}\n<--Метка {arg} не определена')
        self.convert_flag = False

    def invalid_register(self,arg):
        self.con.print(f'L{self.lineN}: {self.line}\n<--Неверное имя регистра {arg}')
        self.convert_flag = False

    def not_arg(self,arg,descr):
        self.con.print(f'L{self.lineN}: {self.line}\n<--Недостаточно аргументов {arg} _<--ожидается {descr}')
        self.convert_flag = False

    def value_ovrfl(self,arg):
        self.con.print(f'L{self.lineN}: {self.line}\n<--Переполнение {self.width}-х битного целого числа {arg}, число больше {self.max_number}')
        self.convert_flag = False

    def sys_invalid_literal(self,arg):
        self.con.print(f'L{self.lineN}: {self.line}\n<--Hеверный символ {arg}')
        self.convert_flag = False

    def bad_expression_bias(self,exp, str):
        self.con.print(f'L{self.lineN}: {self.line}\n<--Выражение {exp} >> {str}')
        self.convert_flag = False

    def get_register(self,name):
        if name in self.REGISTERS:
            return self.REGISTERS[name]
        else:
            if self.convert_flag:
                self.invalid_register(name)
            return 0

    def get_label(self,name):
        if name in self.LABELS:
            return self.LABELS[name]
        else:
            if self.convert_flag:
                self.no_label_error(name)
            return 0

    def get_command(self,name):
        if name in self.COMMANDS:
            command = self.COMMANDS[name]
        else:
            self.no_comma_error(name)
            return 0

        if isinstance(command, list):
            return command
        if command == 'spec':
            return command

        if isinstance(command, str):
            try:
                return self.ebal(command)
            except Exception as e:
                self.con.print(f"Ошибка вычисления команды '{name}': {e}")
                self.convert_flag = False
                return [0x00, 0x00]

        if callable(command):
            return command()

        else:
            if self.convert_flag:
                self.no_comma_error(name)
            return [0x00, 0x00]
    # EVAL !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def ebal(self, expression):

        cache_key = f"{expression}_{self.arg1}_{self.arg2}_{self.arg3}"
        if cache_key in self._eval_cache:
            return self._eval_cache[cache_key]

        self.names = {
            'arg1': self.arg1,
            'arg2': self.arg2,
            'arg3': self.arg3,
            'arg4': self.arg4,
            'self': self,
        }

        result = simple_eval(expression,functions=self.functions,names=self.names)
        self._eval_cache[cache_key] = result
        return result

    def convert(self):
        self.ttl = time.time()
        self.convert_flag = True
        self.memADR = 0

        print(f'{round((time.time()-self.ttl)*1000,2)}мс: Пре-ассемблирование и добавление меток')
        while self.lineN < len(self.raw) and self.convert_flag: #пре-ассемблирование добавление меток
            self.line = self.raw[self.lineN]
            self.line = self.line.replace('\t', '')
            if not self.line.startswith(';') and not self.line == '':
                parse_line = self.line.split(';')[0]
                parse_line = parse_line.split()

                if parse_line[0] == 'fn:':
                    if len(parse_line) > 1:
                        self.LABELS[parse_line[1]] = self.memADR
                    else:
                        self.not_arg(parse_line[0],'label')

                elif parse_line[0] == '#define':
                    if len(parse_line) > 2:
                        self.LABELS[parse_line[1]] = self.number_string(parse_line[2])
                    else:
                        self.not_arg(parse_line[0],'label , value')

                elif parse_line[0] == 'data=':
                    if len(parse_line) == 3:
                        self.LABELS[parse_line[1]] = self.memADR
                        self.memADR += 16
                    else:
                        self.not_arg(parse_line[0],'label')


                elif parse_line[0] == ':':
                    if len(parse_line) > 1:
                        if self.number_string(parse_line[1]) > self.memADR:
                            self.memADR = self.number_string(parse_line[1])
                        else:
                           self.con.print(f'L{self.lineN}: {self.line}\n<--Ожидается адрес менее {self.memADR}')
                    else:
                        self.not_arg(parse_line[0],'"указатель адреса"')

                else:
                    self.memADR += self.get_len(parse_line[0]) * self.insruction_len
            self.lineN += 1

        print(f'{round((time.time() - self.ttl) * 1000, 2)}мс: Пре-ассемблирование и добавление меток - pass')
        self.lineN = 0
        self.memADR = 0
        while self.lineN < len(self.raw) and self.convert_flag:
            self.percent_to_complite += self.percent_of_line
            self.progressbar(self.percent_to_complite)

            self.line = self.raw[self.lineN]
            self.line = self.line.replace('\t', '')
            if not self.line.startswith(';') and not self.line == '':
                parse_line = self.line.split(';')[0]
                parse_line = parse_line.split()
                self.arg1 = compiler.get_ind(parse_line,1)
                self.arg2 = compiler.get_ind(parse_line,2)
                self.arg3 = compiler.get_ind(parse_line,3)
                self.arg4 = compiler.get_ind(parse_line,4)

                if self.get_command(parse_line[0]) != 'spec':
                    conv = self.get_command(parse_line[0])
                    quit = []

                    for i in range(0,self.insruction_len * self.get_len(parse_line[0]),1):
                        quit.append((conv >> (self.width * i)) & self.max_number)

                    self.output_memory(quit)
                    self.memADR += self.get_len(parse_line[0]) * self.insruction_len

                elif parse_line[0] == ':':
                    self.memADR = self.number_string(parse_line[1])

                elif parse_line[0] == 'data=':
                    if self.arg2 != '':
                        q = []
                        for i in self.arg2.split(','):
                            q.append(self.number_string(i))
                        self.output_memory(q)
                    else:
                        self.not_arg(parse_line[0],'список чисел')
                    self.memADR += 16

            self.lineN += 1
        self.out_len = self.memADR

        return 0

    def buld_damb(self):
        if self.convert_flag:
            print(f'{round((time.time() - self.ttl) * 1000, 2)}мс: Сборка дампа')
            self.con.print(f'\n{round((time.time() - self.ttl) * 1000, 2)}мс: Сборка дампа')
        #init
        damb = ['v2.0 raw']
        for i in range(self.out_len):
            damb.append(0)
        for j in range(0,len(self.out),1):
            adr = self.out[j][0] + 1
            data = self.out[j][1]
            damb[adr] = self.to_hex(data)
        if self.convert_flag:
            print(f'{round((time.time() - self.ttl) * 1000, 2)}мс: Сборка дампа - pass')
            self.con.print(f'\n{round((time.time() - self.ttl) * 1000, 2)}мс: Сборка дампа - pass')
        if self.format == 'Logisim':
            if self.convert_flag:
                self.con.print('\n')
                self.con.print(f'Успешная компиляция за {round((time.time() - self.ttl) * 1000)} мс', end='\n')
                self.con.print(f'\n{compiler.get_weight(len(damb))}B / {compiler.get_weight(self.mem)}B {round(len(damb) / self.mem * 100,2)}% type: Logisim')
                self.convert_flag = False
            else:
                self.con.print('\n\nTRACEBACK')

        elif self.format == 'bin':

            fmt = {
                4: 'B',
                8: 'B',
                16: 'H',
                32: 'I',
                64: 'Q',
            }

            try:

                format_num = fmt.get(self.width)

                damb.remove('v2.0 raw')
                byte_list = []

                for num in damb:
                    byte_list.append(struct.pack(format_num, int(num,16)))

                damb = b''.join(byte_list)
                if self.convert_flag:
                    self.con.print('\n')
                    self.con.print(f'Успешная компиляция за {round((time.time() - self.ttl) * 1000)} мс', end='\n')
                    self.con.print(f'\n{compiler.get_weight(len(damb))}B / {compiler.get_weight(self.mem)}B {round(len(damb) / self.mem * 100, 2)}% type: Byte')
                    self.convert_flag = False
                else:
                    self.con.print('\n\nTRACEBACK')

            except Exception as e:
                self.con.print('битый префаб')
        return damb

    @staticmethod
    def get_weight(num):
        if num >= 1073741824:
            return f'{round(num/1073741824,3)}G'
        elif num >= 1048516:
            return f'{round(num/1048516,2)}M'
        elif num >= 4096:
            return f'{round(num / 1024, 1)}K'
        else:
            return f'{num}'




