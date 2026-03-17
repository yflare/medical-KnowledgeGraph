import json
import glob
import os

# 获取所有JSON文件的路径
file_paths = glob.glob(r'D:\2-2\knoledge\big\json\simplified_json\\*.json')

# 用于存储合并后的数据
merged_data = []

# 合并所有JSON文件的数据
for file_path in file_paths:
    print(f"Processing file: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)
            if isinstance(data, list):
                merged_data.extend(data)
            else:
                print(f"Warning: {file_path} does not contain a list, skipping...")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from {file_path}: {e}")

# 打印合并后的数据长度
print(f"Total items after merge: {len(merged_data)}")

# 将合并后的数据保存为一个新的JSON文件
merged_output_file = 'merged_data.json'
with open(merged_output_file, 'w', encoding='utf-8') as file:
    json.dump(merged_data, file, ensure_ascii=False, indent=4)

print(f"All JSON files have been merged into {merged_output_file}")
