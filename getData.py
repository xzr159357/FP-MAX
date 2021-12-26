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
    itemAll : defaultdict[str, set] = {}
    itemAll = defaultdict(set)
    index = 0
    for f in findAllFile(base):
        with open(f) as file:
            data = file.read()
            item_table = ress.get_itemTable(data)
            for _, item in item_table.items():
                itemAll['T' + str(1000 + index)] = item
                index += 1

    return itemAll

if __name__ == '__main__':
    get_trans()