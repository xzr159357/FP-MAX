import os
import re
import ress
from typing import DefaultDict, Dict, List, Tuple
from collections import Counter, defaultdict

# 列出所有文件
def findAllFile(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            if f.endswith('.sql'):
                fullname = os.path.join(root, f)
                yield fullname

# 将解析完的SQL语句写入list
def get_trans():
    base = './join-order-benchmark/' # 文件夹路径
    # itemAll : defaultdict[str, set] = {}
    itemAll = defaultdict(list)
    index = 0
    for f in findAllFile(base):
        with open(f) as file:
            data = file.read()
            item_table = ress.get_itemstable(data)
            # print(item_table)
            for item_name, item in item_table.items():
                # itemAll['T' + str(10000 + index)] = item
                # index += 1
                itemAll[item_name].append(item)

    ansItem = defaultdict(dict)
    for item_name, item in itemAll.items():
        if item_name == '':
           continue
        map = defaultdict(list)
        index = 0
        for data in item:
            map['T' + str(10000 + index)] = data
            index += 1
        ansItem[item_name] = map

    return ansItem

if __name__ == '__main__':
    itemAll = get_trans()
    for item_name, name in itemAll.items():
        print(item_name)
        print(name)