import re
from typing import DefaultDict, Dict, List, Tuple
from collections import Counter, defaultdict




sql = """
   SELECT MIN(mc.note) AS production_note,
       MIN(t.title) AS movie_title,
       MIN(t.production_year) AS movie_year
FROM company_type AS ct,
     info_type AS it,
     movie_companies AS mc,
     movie_info_idx AS mi_idx,
     title AS t
WHERE ct.kind = 'production companies'
  AND it.info = 'top 250 rank'
  AND mc.note NOT LIKE '%(as Metro-Goldwyn-Mayer Pictures)%'
  AND (mc.note LIKE '%(co-production)%'
       OR mc.note LIKE '%(presents)%')
  AND ct.id = mc.company_type_id
  AND t.id = mc.movie_id
  AND t.id = mi_idx.movie_id
  AND mc.movie_id = mi_idx.movie_id
  AND it.id = mi_idx.info_type_id;
    """

# 解析SQL语句
def get_itemTable(sql :str) -> Dict[str, set]:
    pattern = r'\w*[.]\w*'
    fields = re.findall(pattern, sql)
    item_table: DefaultDict[str, set] = {}
    item_table = defaultdict(set)

    for field in fields:
        # 根据'.'分割表和字段
        data = field.split('.', 1)
        item_table[data[0]].add(data[1])
    # 处理为list
    for item, itemsets in item_table.items():
        item_table[item] = [str(itemset) for itemset in itemsets]

    return item_table

# 新SQL解析，处理聚合函数，但是将聚合函数里的item也看做独立的项
def get_itemFunc(sql : str) -> Dict[str, set]:
    # 1.处理普通
    pattern = r'\w*[.]\w*'
    fields = re.findall(pattern, sql)
    item_table : DefaultDict[str, set] = {}
    item_table = defaultdict(set)
    for field in fields:
        # 根据'.'分割表和字段
        data = field.split('.', 1)
        item_table[data[0]].add(data[1])

    # 2.处理聚合函数
    pattern = r'\w*[(]\w*[.]\w*[)]'
    fields = re.findall(pattern, sql)
    for field in fields:
        # 聚合函数
        pat1 = r'\w*[(]'
        data1 = re.search(pat1, field)
        # 列
        pat2 = r'\w*[)]'
        data2 = re.search(pat2, field)
        # 收集的信息
        msg = data1.group() + data2.group()
        # 表名
        pat3 = r'\w*[.]'
        data3 = re.search(pat3, field)
        table_name = data3.group()[:-1]
        item_table[table_name].add(msg)

    # 处理为list
    for item, itemsets in item_table.items():
        item_table[item] = [str(itemset) for itemset in itemsets]

    return item_table

# 全新的SQL处理函数，不将聚合函数里的列看做单独item
def get_itemtable(sql : str) -> Dict[str, set]:
    # 1.处理普通
    pattern = r'[^ ]*[.][^ ]*'
    fields = re.findall(pattern, sql)
    item_table: DefaultDict[str, set] = {}
    item_table = defaultdict(set)
    # pattern，聚合函数测试
    patternTest = r'\w*[(]\w*[.]\w*[)]'
    for field in fields:
        # 根据'.'分割表和字段
        if re.search(patternTest, field) != None:
            # 聚合函数
            pat1 = r'\w*[(]'
            data1 = re.search(pat1, field)
            # 列
            pat2 = r'\w*[)]'
            data2 = re.search(pat2, field)
            # 收集的信息
            msg = data1.group() + data2.group()
            # 表名
            pat3 = r'\w*[.]'
            data3 = re.search(pat3, field)
            table_name = data3.group()[:-1]
            item_table[table_name].add(msg)
        else:
            patt = r'\w*[.]\w*'
            reField = re.search(patt, field)
            field = reField.group()
            data = field.split('.', 1)
            item_table[data[0]].add(data[1])

    # 处理为list
    for item, itemsets in item_table.items():
        item_table[item] = [str(itemset) for itemset in itemsets]
    return item_table

# 20211230更新sql语句解析
def get_itemstable(sql : str) -> Dict[str, set]:
    # 1.处理普通
    pattern = r'[^ ]*[.][^ ]*'
    fields = re.findall(pattern, sql)
    # item_table: DefaultDict[str, set] = {}
    item_table = defaultdict(set)
    # 2.将表名的别名处理为表名
    # 2.1 提取出表名所在字符串
    pattern = r'FROM'
    matchLeft = re.search(pattern, sql)
    pattern = r'WHERE'
    matchRight = re.search(pattern, sql)
    newText = sql[matchLeft.span()[1] : matchRight.span()[0]]
    # print(newText)
    # 2.2 完成别名->表名的哈希表
    pattern = r'\w*[ ]*AS[ ]*\w*' # 将一个个AS语句提取
    datas = re.findall(pattern, newText)
    nickToNameMap = defaultdict(str) # 别名转为列名
    for data in datas:
        arr = data.split(' ')
        table_name = arr[0]
        table_nickName = arr[len(arr) - 1]
        nickToNameMap[table_nickName] = table_name

    # pattern，聚合函数测试
    patternTest = r'\w*[(]\w*[.]\w*[)]'
    for field in fields:
        # 根据'.'分割表和字段
        if re.search(patternTest, field) != None:
            # 聚合函数
            pat1 = r'\w*[(]'
            data1 = re.search(pat1, field)
            # 列
            pat2 = r'\w*[)]'
            data2 = re.search(pat2, field)
            # 收集的信息
            msg = data1.group() + data2.group()
            # 表名
            pat3 = r'\w*[.]'
            data3 = re.search(pat3, field)
            table_name = data3.group()[:-1]
            item_table[nickToNameMap[table_name]].add(msg)
        else:
            patt = r'\w*[.]\w*'
            reField = re.search(patt, field)
            field = reField.group()
            data = field.split('.', 1)
            item_table[nickToNameMap[data[0]]].add(data[1])

    # 处理为list
    for item, itemsets in item_table.items():
        item_table[item] = [str(itemset) for itemset in itemsets]
    return item_table


if __name__ == "__main__":
    item_table = get_itemstable(sql)
    for item, itemset in item_table.items():
        print(item + " , " + str(itemset))
