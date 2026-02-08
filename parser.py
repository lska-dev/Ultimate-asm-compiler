from unittest import case
import yaml

class Parser:
    def __init__(self,patch):
        try:
            with open(patch, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)
                print(data)
                print('parsing prefab..')
                for i in ['memory_space','max_number','width_data','word_order','register_file','instruction_mapping','coding']:
                    print('pass')
                    if i not in data:
                        print('префаб не содержит: {}'.format(i))
                        break
                self.data = data
                self.memory_space = data['memory_space']
                self.max_number = data['max_number']
                self.word_order = data['word_order']
                self.register_file = data['register_file']
                self.instruction_mapping = data['instruction_mapping']
                self.coding = data['coding']

        except yaml.YAMLError as exc:
            print(exc)
        except KeyError as exc:
            print('<UNK> <UNK> <UNK>: {}'.format(exc))

class compiler():
    def __init__(self,patch):
        self.prosessor = Parser(patch)
        self.register_file = self.prosessor.register_file
        self.max_number = self.prosessor.max_number
        self.instruction_mapping = self.prosessor.instruction_mapping
        self.coding = self.prosessor.coding
        self.labels = {'хуй':100}

    def TRACEBACK(self,text):
        print(f'TRACEBACK \n{text}')

    def convert_imm(self,s):
        s = str(s)
        o = s
        try:
            if s.startswith('"') and s.endswith('"'):
                o = s.split('"')[1]
                return ord(o)
            if s.startswith(':'):
                o = self.get('label',s[1:])
                return o
            s = s.lower()
            #отрабатываем СС
            if s.startswith('0x'):
                o = int(s.split('x')[-1], 16)
            if s.startswith('0b'):
                o = int(s.split('b')[-1], 2)
            if s.startswith('0o'):
                o = int(s.split('o')[-1], 8)

            if int(o) < self.max_number:
                return o
            else:
                self.TRACEBACK(f'Overflow: {o} > {self.max_number}')
                return 0
        except ValueError as exp:
            self.TRACEBACK(exp)
            return 0

    def get(self, type, data):
        match type:
            case 'register':
                q = self.register_file[data]
                if q == None:
                    self.TRACEBACK('Invalid register: {}'.format(type))
                return q['index']
            case 'label':
                q = self.labels.get(data)
                if q == None:
                    self.TRACEBACK('Name {} is not defined'.format(type))
                return q
            case 'const':
                return data
            case 'imm':
                return self.convert_imm(data)
            case _:
                return None

    def code(self,instruction,args):
        o = 0
        try:
            if instruction in self.coding:
                coding = self.coding[instruction]
                type_instruction = self.coding[instruction]['type']
                coding.pop('type')
                for k,v in coding.items():
                    arg_parram = self.instruction_mapping[type_instruction][k]
                    if str(v).startswith('arg'):
                        q = self.get(arg_parram['mode'], args[int(v.split('g')[-1])])
                    else:
                        q = self.get(arg_parram['mode'],v)
                    print(q, k, int(str(v).split('g')[-1]))
                    q = int(q) << arg_parram['offset'] & arg_parram['len']
                    o = o | q
        except KeyError as exp:
            print(exp)




c = compiler('R232.yaml')
c.code('sb',['x5'])