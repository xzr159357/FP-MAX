# 一、说明

- FP-MAX是最大频繁项挖掘的算法

- fpgrowth是频繁项挖掘的算法
- ress.py处理SQL语句
- getData.py将ress处理的结果写入List
- join-order-benchmark里是处理的SQL语句



# 二、算法

## FP-growth

**FP-growth**(频繁模式增长)算法是韩家炜老师在2000年提出的关联分析算法，它采取如下**分治**策略：将提供频繁项集的数据库压缩到一棵频繁模式树（FP-Tree），但仍保留项集关联信息。该算法和Apriori算法最大的不同有两点：第一，不产生候选集，第二，只需要两次遍历数据库，大大提高了效率。



## FP-MAX

FP-MAX算法在FP-growth的基础上，通过构建类似于FP-tree的MFI-tree，实现最大频繁项的数据处理。
