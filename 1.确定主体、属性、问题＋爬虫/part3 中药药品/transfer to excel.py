import pandas as pd  
import openpyxl

# 读取JSON文件  
data = pd.read_json('E:\\爬虫学习\\中医问答爬虫\\part2\\h2完整.json')   
  
# 将数据保存为Excel文件，不包含索引列  
data.to_excel('h2完整.xlsx', index=False)
