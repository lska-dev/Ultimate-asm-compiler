#  UDL generator
from atexit import register


def read(path):
    with open(path, "r", encoding = "UTF-8") as file:
       return file.read()

"""  Class Processor/parram  """
def convert(parram):
    try:
        xml = read("UDL/default.udl.xml")
    except FileNotFoundError:
        print("missing 'UDL/default.udl.xml'")
        return 0
    try:
        registers = ""
        for reg in  parram.REGISTERS:
            registers = registers + reg + " "
        commands = ""
        for com in parram.COMMANDS:
            if not com in ["fn:","#define","data=",":"]:
                commands = commands + com + " "
        name = parram.name
    except NameError as e:
        print(f"processor invalid {e}")
        return 0

    xml = xml.replace("USER_REGS", registers)
    xml = xml.replace("USER_COMMANDS", commands)

    with open(f"processors/{name}.udl.xml", "w+", encoding="UTF-8") as file:
        file.write(xml)

