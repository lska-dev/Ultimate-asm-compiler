from simpleeval import simple_eval
import compiler
import tkinter as tk
import time
from tkinter import filedialog, scrolledtext, ttk, messagebox
import os
import sys
import importlib.util

class ModuleLoader:
    """Загрузчик модулей для работы в EXE"""

    def __init__(self):
        self.modules_cache = {}
        self.discover_modules()

    def discover_modules(self):
        """Находит все .py файлы в нужных директориях"""
        self.available_modules = []

        if getattr(sys, 'frozen', False):
            # В EXE - ищем в _MEIPASS и рядом с EXE
            search_paths = [sys._MEIPASS, os.path.dirname(sys.executable)]
        else:
            # В Python - ищем в директории скрипта
            search_paths = [os.path.dirname(os.path.abspath(__file__))]
        for path in search_paths:
            if os.path.exists(path):
                for root, dirs, files in os.walk(path):
                    for file in files:
                        if file.endswith('.py') and not file.startswith('__'):
                            module_name = file[:-3]  # Без .py
                            full_path = os.path.join(root, file)
                            self.available_modules.append((module_name, full_path))

    def import_module(self, module_name):
        """Импортирует модуль по имени"""
        if module_name in self.modules_cache:
            return self.modules_cache[module_name]

        # Ищем модуль среди обнаруженных
        for name, path in self.available_modules:
            if name == module_name:
                spec = importlib.util.spec_from_file_location(name, path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                self.modules_cache[module_name] = module
                return module

        # Пробуем стандартный импорт
        try:
            module = importlib.import_module(module_name)
            self.modules_cache[module_name] = module
            return module
        except ImportError:
            raise ImportError(f"Модуль '{module_name}' не найден")

out = []
convert = False
color_shem={'bg': '#191919', 'abg': '#303030', 'text': '#ffffff', 'akc': '#376077'}
type = 'Logisim'
file = ''
frame_time = 0

layouts = os.listdir('processors') + os.listdir('.')
prefabs = [f.split('.')[0] for f in layouts if f.endswith('.py') or f.endswith('.pyw')]


if 'compiler' in prefabs:
    prefabs.remove('compiler')
if 'universal assmebly compiler' in prefabs:
    prefabs.remove('universal assmebly compiler')
print(prefabs)

def theme():
    global color_shem,thm
    print(thm.get())
    if thm.get():
        color_shem={'bg': '#191919', 'abg': '#303030', 'text': '#ffffff', 'akc': '#376077'}
        ok = 1
    else:
        color_shem={'bg': '#c0c0c0', 'abg': '#808080', 'text': '#000000', 'akc': '#376077'}
        ok = 0
    apply_theme()
    print(color_shem)
    try:
        fc = open('res/config.txt','r')
        config = fc.read()
        config = f'{ok},{config[-1]}'
        fc.close()
        fc = open('res/config.txt','w')
        fc.write(config)
    except Exception:
        print('конфиг утерян или поврежден')

    return

def set_type():
    global type,r
    if r.get():
        type = 'Logisim'
        ok = 1
    else:
        type = 'Bin'
        ok = 0

    try:
        fc = open('res/config.txt','r')
        config = fc.read()
        config = f'{config[0]},{ok}'
        fc.close()
        fc = open('res/config.txt','w')
        fc.write(config)
    except Exception:
        print('конфиг утерян или поврежден')

def fopen():
    global file
    file = filedialog.askopenfilename(filetypes = (("asembly files","*lasm"),("all files","*.*")))
    name = file.split('/')[-1]
    print(len(name))
    if len(name.split('.')[0]) > 15:
        name = f'{name[0:15]}..{name.split('.')[-1]}'
    if file != '':albl.config(text=name)

def fsave():
    if convert:
        tk.messagebox.showinfo('','Дождитесь конца компиляции')
    else:
        if not out:
            tk.messagebox.showinfo('','Нет данных для сохранения')
        else:
            if r.get():
                flsv = filedialog.asksaveasfile(mode="w+")
                flsv.write('\n'.join(str(item) for item in out))
                flsv.close()
            else:
                flsv = filedialog.asksaveasfile(mode="wb+")
                flsv.write(out)
                flsv.close()


def compile():
    global file,out,convert
    prefabs = [f.split('.')[0] for f in os.listdir('.') if f.endswith('.py') or f.endswith('.pyw')]

    if 'compiler' in prefabs:
        prefabs.remove('compiler')
    else:
        print('ВЕРНИ МНЕ compiler.py')

    types = {
        False: 'bin',
        True: 'Logisim',
    }

    type = r.get()

    if file != '':
        try:
            f = open(file, 'r',encoding='utf-8')
            txt = f.read()
            f.close()
            convert = True
            loader = ModuleLoader()

            mds_module = loader.import_module(select_prefab.get())
            params = mds_module.parram()
            if params.width in[4,8,32,64]:

                compl = compiler.compiler(txt,params,console_command=con_print,format=types[type])
                compl.convert()

                convert = False
                out = compl.buld_damb()
            else:
                messagebox.showerror('ОШИБКА','Неверная разрядность предустановки')
        except Exception as ex:
            messagebox.showerror('ОШИБКА',f'Ошибка предустановки: {str(ex).replace('module','prefab')}')
    else:
        messagebox.showerror('ОШИБКА','Выберете файл источник')

window = tk.Tk()

window.config(bg=color_shem['bg'])
window.title("compiler")
window.geometry("400x400")
window.iconbitmap('res/ico.ico')
window.resizable(False, False)

try: #пользовательская конфигурация
    fc = open('res/config.txt', 'r')
except FileNotFoundError:
    fc = open('res/config.txt', 'w+')
    fc.write('1,1')
    fc.close()
    fc = open('res/config.txt', 'r')
config = []
for i in fc.read().split(','):
    if i == '1':config.append(True)
    else:config.append(False)
fc.close()

r = tk.BooleanVar()
con = tk.StringVar()
thm = tk.BooleanVar()
thm.set(config[0])
r.set(config[1])

frame = tk.Frame(master=window,bg=color_shem.get('bg'))
frame.pack(anchor='w',pady=10)

frameAsm = tk.Frame(master=window,bg=color_shem.get('bg'))
frameAsm.place(x=200,y=10)

frameCons = tk.Frame(master=window,bg=color_shem.get('bg'))
frameCons.pack(anchor='n',fill='x')

style = ttk.Style()
style.theme_use('default')

style.configure("TCombobox",
                fieldbackground=color_shem['abg'],  # Цвет фона выпадающего списка
                background=color_shem['abg'],  # Цвет фона поля
                foreground=color_shem['text'],  # Цвет шрифта
                selectbackground=color_shem['abg'],  # Цвет фона при выборе
                selectforeground=color_shem['text']  # Цвет шрифта при выборе
                )

albl = ttk.Label(frameAsm,text="выберете файл  ",justify=tk.RIGHT,background=color_shem['bg'],foreground=color_shem['text'])
albl.pack(side=tk.LEFT)

button = ttk.Button(frameAsm, text="compile",command=compile,)
button.pack(side="left",padx=10)

lbl = ttk.Label(frame, text="предустановки",
                background=color_shem['bg'],
                foreground=color_shem['text'])
lbl.pack(side='left', padx=10)

select_prefab = tk.StringVar(value=prefabs[0])
prefab_scrollbar = ttk.Combobox(frame,
                                values=prefabs,width=10,
                                textvariable=select_prefab,
                                state="readonly",
                                justify="center",
                                style="TCombobox")
prefab_scrollbar.pack(anchor='n',padx=10,pady=5)

console = scrolledtext.ScrolledText(frameCons,
                                    width=10,height=20,
                                    background=color_shem['abg'],
                                    foreground=color_shem['text'],
                                    selectbackground=color_shem['akc'],
                                    )
console.pack(fill='x')

menu = tk.Menu(window)
item = tk.Menu(menu,background=color_shem['abg'],foreground=color_shem['text'],activebackground=color_shem['akc'])
item.add_command(label='Открыть',command=fopen,)
item.add_command(label='Сохранить',command=fsave,)
menu.add_cascade(label='Файл', menu=item,background=color_shem['abg'],foreground=color_shem['text'],activebackground=color_shem['akc'])
set = tk.Menu(menu,background=color_shem['abg'],foreground=color_shem['text'],activebackground=color_shem['akc'])
set.add_checkbutton(label='темная тема',variable=thm,command=theme)
type = tk.Menu(set,background=color_shem['abg'],foreground=color_shem['text'],activebackground=color_shem['akc'])
type.add_radiobutton(label='logisim \nmemory',variable=r,value=True,command=set_type)
type.add_radiobutton(label='bin file',variable=r,value=False,command=set_type)
set.add_cascade(label='Тип файла',menu=type,background=color_shem['abg'],foreground=color_shem['text'],activebackground=color_shem['akc'])
menu.add_cascade(label='Настройки', menu=set,background=color_shem['abg'],foreground=color_shem['text'],activebackground=color_shem['akc'])
window.config(menu=menu,bg=color_shem['bg'])

def con_print(str):
    global frame_time
    global file
    if frame_time == 0:
        frame_time = time.time()
    console.delete(1.0,tk.END)
    console.insert(tk.INSERT,f'{file}\n{str}')
    if time.time()-frame_time > 1/30:
        console.update()
        frame_time = time.time()

def apply_theme():
    window.config(bg=color_shem['bg'])
    frame.config(bg=color_shem['bg'])
    frameAsm.config(bg=color_shem['bg'])
    frameCons.config(bg=color_shem['bg'])

    albl.config(background=color_shem['bg'], foreground=color_shem['text'])
    lbl.config(background=color_shem['bg'], foreground=color_shem['text'])

    console.config(background=color_shem['abg'],
                   foreground=color_shem['text'],
                   selectbackground=color_shem['akc'])

    style.configure("TCombobox",
                    fieldbackground=color_shem['abg'],
                    background=color_shem['abg'],
                    foreground=color_shem['text'],
                    selectbackground=color_shem['abg'],
                    selectforeground=color_shem['text'])

theme()

window.mainloop()
