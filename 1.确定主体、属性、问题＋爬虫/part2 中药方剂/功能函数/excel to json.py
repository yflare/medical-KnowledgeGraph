import pandas as pd

# 读取Excel文件
excel_file = 'E:\\爬虫学习\\中医问答爬虫\\part2\\C.xlsx'
sheet_name = 'Sheet1'  # 或者您想要读取的工作表的名称
df = pd.read_excel(excel_file, sheet_name=sheet_name)

# 将DataFrame转换为JSON
json_data = df.to_json(orient='records')

# 将JSON数据写入文件
with open('h2_C完整清洗.json', 'w', encoding='utf-8') as f:
    f.write(json_data)
