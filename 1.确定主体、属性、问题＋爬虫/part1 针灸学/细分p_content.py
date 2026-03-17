import json
import re

# 读取原始 JSON 文件
with open('h2_p_contents.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 定义正则表达式模式，用于匹配不同的部分
patterns = {
    '主证': re.compile(r'1\. 主证：(.*?)$'),
    '治法': re.compile(r'2\. 治法：(.*?)$'),
    '处方': re.compile(r'3\. 处方：(.*?)$')
}

# 遍历数据，细分 p_contents
for item in data:
    p_contents = item.get('p_contents', [])
    if p_contents:
        new_contents = {}
        text = '\n'.join(p_contents).strip()
        for key, pattern in patterns.items():
            match = pattern.search(text)
            if match:
                new_contents[key] = match.group(1).strip()
        item.update(new_contents)
        del item['p_contents']

# 写入新的 JSON 文件
with open('常见病症.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print('处理完成')
