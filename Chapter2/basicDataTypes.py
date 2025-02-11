import pprint
from os import system

system('clear')

def print_variable_id(variable, variable_name):
    text_color = "\033[32m"
    id_color = "\033[m"
    print(text_color + "{0} id:".format(variable_name)+ id_color + "{0}".format(id(variable)))

print("Hello")
mystr = "tom"
print_variable_id(mystr, "mystr")

a = 2
b = 3

print("{1} a+b= {0}".format(a+b, chr(26)))

ascii_code_list = {}

for i in range(1, 255):
    code_number = i
    chr_str = "chr({0}) prints {1}".format(i, chr(i))
    ascii_code_list.update({code_number: chr_str})

prettyprint = pprint.PrettyPrinter(indent=5, width=100, compact=True)
prettyprint.pprint(ascii_code_list)

device_name = "Monnit Temparature sensor"

print("data type of device_name is {0}".format(type(device_name)))

print(f"data type is device_name is {type(device_name)}")