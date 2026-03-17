import json
with open('part2/h1.json', 'r', encoding='utf-8') as file:  
    h1_data = json.load(file)

# 创建一个新的字典，用于存储新的JSON结构
new_json = {"h2_links": []}

# 遍历原始数据，将链接添加到新的JSON结构中
for item in h1_data:
    new_json["h2_links"].append(item["h2_links"])

# 将新的JSON结构转换为字符串，并写入文件
with open("h1.json", "w", encoding="utf-8") as file:
    json.dump(new_json, file, ensure_ascii=False, indent=4)

print("JSON文件已创建。")
