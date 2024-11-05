import urllib.request
from lxml import etree

'''
2023-06:52,2023-05:49,2023-04:41,2023-03:41,2023-02:36,2023-01:33,
2022-12:44,2022-11:40,2022-10:37,2022-09:38,2022-08:36,2022-07:33,2022-06:34j
'''

# url拼接 基础URL
base_url = 'https://xl.16888.com/city-2022-06-0-0-57328-0-0-'
#
# for i in range(1, 53):
#     url = base_url + str(i) + '.html'
#     print(url)

# 数据获取到列表 range()为页数加1
byd_2023_06_list = []
span_2023_06_list = []

for i in range(1, 35):
    url = base_url + str(i) + '.html'
    response = urllib.request.urlopen(url)
    html = response.read().decode('utf-8')
    parse_html = etree.HTML(html)
    xpath_bds = '//div//tbody/tr//a/text() | //div//tbody/tr//a/em/text()'
    xpath_span = '//div//tbody//td/a/span/text()'
    byd_base_list = parse_html.xpath(xpath_bds)
    span_base_list = parse_html.xpath(xpath_span)
    # print(byd_list)
    # 获取到的数据每次都添加到byd_2023_06_list的后面 extend()方法追加到列表后面
    byd_2023_06_list.extend(byd_base_list)
    span_2023_06_list.extend(span_base_list)

# print(byd_2023_06_list)
# print(span_2023_06_list)
# print(len(byd_2023_06_list)/6)
# print(len(span_2023_06_list))

# span数据的处理
byd_span_list = []

for i in span_2023_06_list:
    byd_span_list.append(i.split('-'))

# print(byd_span_list)
# print(len(byd_2023_06_list) / 6)
# print(len(span_2023_06_list))
# print(len(byd_span_list))

# 组成最终数据
for i in range(0, len(byd_2023_06_list), 6):
    j = int(i / 6)
    byd_2023_06_list[i + 4] = byd_span_list[j][0]
    byd_2023_06_list[i + 5] = byd_span_list[j][1]

# print(byd_2023_06_list)

# 最终数据处理，获取想要的格式
byd_list = []

for i in range(0, len(byd_2023_06_list), 6):
    tup = (byd_2023_06_list[i], byd_2023_06_list[i+1], byd_2023_06_list[i+2], byd_2023_06_list[i+3],
           byd_2023_06_list[i+4], byd_2023_06_list[i+5])
    byd_list.append(tup)

print(byd_list)
print(len(byd_list))
# tuple类型
# print(type(byd_list[0]))

# byd_list写入到.csv中
with open('data/byd_2022_06.csv', 'w', encoding='utf-8') as f:
    for i in byd_list:
        f.write(','.join(i) + '\n')
