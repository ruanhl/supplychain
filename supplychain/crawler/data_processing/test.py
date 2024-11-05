import csv

city_list = []

# 打开CSV文件并读取数据
with open(r'E:\forecast\crawler\data\city.csv', 'r', encoding='utf-8') as file:
    city = csv.reader(file)
    for row in city:
        city_list.append(row)

# print(city_list)


def get_idx(city_name):
    for j in range(0,len(city_list)):

        if city_name == city_list[j][2]:
            return j


byd = []

byd_list = []

with open(r'E:\forecast\crawler\data\byd_2022_06.csv', 'r', encoding='utf-8') as file:
    byd_0 = csv.reader(file)
    for row in byd_0:
        row.extend('0')
        byd_list.append(row)

with open(r'E:\forecast\crawler\data\byd_2022_07.csv', 'r', encoding='utf-8') as file:
    byd_1 = csv.reader(file)
    for row in byd_1:
        row.extend('1')
        byd_list.append(row)

with open(r'E:\forecast\crawler\data\byd_2022_08.csv', 'r', encoding='utf-8') as file:
    byd_2 = csv.reader(file)
    for row in byd_2:
        row.extend('2')
        byd_list.append(row)

with open(r'E:\forecast\crawler\data\byd_2022_09.csv', 'r', encoding='utf-8') as file:
    byd_3 = csv.reader(file)
    for row in byd_3:
        row.extend('3')
        byd_list.append(row)

with open(r'E:\forecast\crawler\data\byd_2022_10.csv', 'r', encoding='utf-8') as file:
    byd_4 = csv.reader(file)
    for row in byd_4:
        row.extend('4')
        byd_list.append(row)

with open(r'E:\forecast\crawler\data\byd_2022_11.csv', 'r', encoding='utf-8') as file:
    byd_5 = csv.reader(file)
    for row in byd_5:
        row.extend('5')
        byd_list.append(row)

with open(r'E:\forecast\crawler\data\byd_2022_12.csv', 'r', encoding='utf-8') as file:
    byd_6 = csv.reader(file)
    for row in byd_6:
        row.extend('6')
        byd_list.append(row)

with open(r'E:\forecast\crawler\data\byd_2023_01.csv', 'r', encoding='utf-8') as file:
    byd_7 = csv.reader(file)
    for row in byd_7:
        row.extend('7')
        byd_list.append(row)

with open(r'E:\forecast\crawler\data\byd_2023_02.csv', 'r', encoding='utf-8') as file:
    byd_8 = csv.reader(file)
    for row in byd_8:
        row.extend('8')
        byd_list.append(row)

with open(r'E:\forecast\crawler\data\byd_2023_03.csv', 'r', encoding='utf-8') as file:
    byd_9 = csv.reader(file)
    for row in byd_9:
        row.extend('9')
        byd_list.append(row)

with open(r'E:\forecast\crawler\data\byd_2023_04.csv', 'r', encoding='utf-8') as file:
    byd_10 = csv.reader(file)
    data = ['10']
    for row in byd_10:
        row.extend(data)
        byd_list.append(row)

with open(r'E:\forecast\crawler\data\byd_2023_05.csv', 'r', encoding='utf-8') as file:
    byd_11 = csv.reader(file)
    data = ['11']
    for row in byd_11:
        row.extend(data)
        byd_list.append(row)

with open(r'E:\forecast\crawler\data\byd_2023_06.csv', 'r', encoding='utf-8') as file:
    byd_12 = csv.reader(file)
    data = ['12']
    for row in byd_12:
        row.extend(data)
        byd_list.append(row)

# print(byd_list)

for i in range(0, len(byd_list)):
    try:
        idx = get_idx(byd_list[i][1])
    except TypeError:
        print(byd_list[i][1])
        continue
    try:
        tup = (byd_list[i][6], city_list[idx][0], city_list[idx][1], byd_list[i][0], str(round(float(byd_list[i][4]))),
               str(round(float(byd_list[i][5]))), byd_list[i][2])
    except TypeError:
        print(byd_list[i])
        continue
    byd.append(tup)

# print(byd)

with open('byd.csv', 'w', encoding='utf-8') as f:
    for i in byd:
        f.write(','.join(i) + '\n')

'''
list_1 = df.head().values.tolist()

for i in list_1:
    print(i)
    for j in i: reader = csv.reader(file)
    for row in reader:
        print(row)
        # print(j)
        print(type(j))
['汉', '深圳', 1596, '中大型车', 21.48, 32.98]
<class 'str'>
<class 'str'>
<class 'int'>
<class 'str'>
<class 'float'>
<class 'float'>
'''
