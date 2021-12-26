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


if __name__ == "__main__":
    item_table = get_itemTable(sql)
    for item, itemset in item_table.items():
        print(item + " , " + str(itemset))
