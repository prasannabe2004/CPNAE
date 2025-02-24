from tabulate import tabulate
import pandas
import pprint
from os import system
from sys import getsizeof
import timeit

# List
temperatures = [98.64, 98.62, 98.57, 98.54, 98.61, 49.70, 98.61, 98.53, 98.60]

variance = []
labels = []

i = 1

for t in temperatures:
    variance.append(round(t - 98.6, 2))
    labels.append("Temparature ({0})".format(str(i)))
    i+=1

table_tuple = list(zip(labels, temperatures, variance))
print(table_tuple)
dataframe = pandas.DataFrame(table_tuple, columns=['labels', 'Temperature', 'Variance'])

print(dataframe)

print("\n{0}\n".format(dataframe.iloc[5:]))

print('\n'+ tabulate(dataframe, showindex=False, headers="keys", tablefmt="fancy_grid"))


#Tuple
movement=(1,0,1,0,1,1,0,1,1,1,0,1,1,0,1,0,1,1,1,0,1,0,1,1,0,1,0,1,0,1)

moved = 0
for moving in movement:
    if moving == 1:
        moved += 1

moved_percent = round(moved/len(movement)*100, 2)
prettyprint = pprint.PrettyPrinter(width=82, compact=True)
prettyprint.pprint(movement)

print(moved_percent)

# Dict
iot_device = {"device1": "temparature sensor", "device2" : "motion sensor", "device3": "light sensor"}

print("iot_devices type = {0} and data {1}".format(type(iot_device), iot_device))
print("device 2 is", iot_device["device2"])

# Set
myset = {1,2,3,4,5}
print("the set of type {} and data is {}".format(type(myset), myset))

myfrozenset = frozenset(myset)
print("the set of type {} and data is {}".format(type(myfrozenset), myfrozenset))

listsize = [1,2,3,4,5, "horse", "cow", "donkey", "dog", "elephant"]
tuplesize = (1,2,3,4,5, "horse", "cow", "donkey", "dog", "elephant")
setsize = {1,2,3,4,5, "horse", "cow", "donkey", "dog", "elephant"}
frozensetsize = frozenset(setsize)

print("size of list" , getsizeof(listsize))
print("size of tuple" , getsizeof(tuplesize))
print("size of set" , getsizeof(setsize))
print("size of frozenset" , getsizeof(frozensetsize))

listtime = '''
listforsize = [1,2,3,4,5,6,7,8,9,8,7,6,5,4,3,2,1,2,3,4,5,6,7,8,9]
for i in listforsize:
    result = i * 3
'''

tupletime = '''
listforsize = (1,2,3,4,5,6,7,8,9,8,7,6,5,4,3,2,1,2,3,4,5,6,7,8,9)
for i in listforsize:
    result = i * 3
'''

settime = '''
listforsize = {1,2,3,4,5,6,7,8,9,8,7,6,5,4,3,2,1,2,3,4,5,6,7,8,9}
for i in listforsize:
    result = i * 3
'''

print("list perf is  {}".format(round(timeit.timeit(stmt=listtime ,number=1000000),2)))
print("tuple perf is {}".format(round(timeit.timeit(stmt=tupletime,number=1000000),2)))
print("set perf is   {}".format(round(timeit.timeit(stmt=settime  ,number=1000000),2)))