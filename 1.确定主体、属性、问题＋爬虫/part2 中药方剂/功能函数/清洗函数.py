import json  
  
def clean_json(json_data):  
    cleaned_data = []  
    seen_links = set()  
  
    for item in json_data:  
        if 'title' in item and 'h3_link' in item:  
            # 正常项，包含title和h3_link  
            cleaned_data.append(item)  
        elif 'h3_link' in item:  
            # 只有h3_link，检查其值  
            link = item['h3_link']  
            if link.startswith(('http://', 'https://', '/')):  
                # 链接以http://, https://, 或 / 开头，保留  
                if link not in seen_links:  
                    cleaned_data.append(item)  
                    seen_links.add(link)  
  
    return cleaned_data  
  
# 读取JSON文件  
with open('part2/h2完整.json', 'r', encoding='utf-8') as f:  
    data = json.load(f)  
  
# 清洗数据  
cleaned_data = clean_json(data)  
  
# 写入新的JSON文件  
with open('h2_clean.json', 'w', encoding='utf-8') as f:  
    json.dump(cleaned_data, f, ensure_ascii=False, indent=4)