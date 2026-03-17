from rdflib import Graph

# 加载第一个TTL文件
g1 = Graph()
g1.parse("teacher.ttl", format="turtle")

# 加载第二个TTL文件
g2 = Graph()
g2.parse("drug.ttl", format="turtle")

# 合并两个图
g1 += g2

# 保存合并后的图为新的TTL文件
g1.serialize(destination="combined.ttl", format="turtle")
