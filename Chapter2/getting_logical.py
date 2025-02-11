import os.path
import csv
#from custom_functions import check_validity

a = 5
b = a
c = 4

d = False

if d == True:
    print(f"d is true = {d}")
else:
    print(f"d is false {d}")


if os.path.exists("data.txt"):
    with open('data.txt', 'r') as data_file:
        data_raw = data_file.readline()
    file_exists = True
else:
    print("file does not exists")
    file_exists = False

if file_exists:
    print(data_raw)
    data_list = data_raw.split()
    uniq_values = len(set(data_list))
    print(data_list)
    print(len(data_list))
    print(uniq_values)

with open('formatted_data.txt', 'w') as data_file:
    csv_writer = csv.writer(data_file)
    csv_writer.writerow(data_list)
