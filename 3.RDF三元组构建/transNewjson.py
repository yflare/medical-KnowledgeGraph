import json

# 原始JSON数据文件路径
input_file = r'D:\2-2\knoledge\big\json\h3切分json\h3_TWX完整.json'

# 简化后的JSON数据文件路径
output_file = r'D:\2-2\knoledge\big\json\simplified_json\h3_TWX完整.json'

# 读取原始JSON数据
with open(input_file, 'r', encoding='utf-8') as file:
    data = json.load(file)

# 字段映射：中文字段名到英文字段名
field_mapping = {
    "title": "name",
    "处方": "prescription",
    "功能主治": "function",
    "用法用量": "usage",
    "注意": "note",
    "别名": "alias",
    "制法": "preparation",
    "临床应用": "clinical_application"
}


# 用于去重的集合
unique_items = set()

# 过滤并简化数据
simplified_data = []
for item in data:
    simplified_item = {field_mapping[key]: item.get(key) for key in field_mapping}
    
    
    # 转换成不可变类型以便于去重
    item_tuple = tuple((k, tuple(v) if isinstance(v, list) else v) for k, v in simplified_item.items())
    if item_tuple not in unique_items:
        unique_items.add(item_tuple)
        simplified_data.append(simplified_item)

# 将简化后的数据写入新的JSON文件
with open(output_file, 'w', encoding='utf-8') as file:
    json.dump(simplified_data, file, ensure_ascii=False, indent=4)


print("已经保存新处理的信息到json文件！")
