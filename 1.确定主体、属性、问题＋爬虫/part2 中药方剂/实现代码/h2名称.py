import requests
from bs4 import BeautifulSoup
import json

# 读取h1.json文件
with open('part2/h1.json', 'r', encoding='utf-8') as file:
    h1_data = json.load(file)

# 存储结果的列表
h2_data = []

if 'h2_links' in h1_data:
    # 遍历h1_data中的链接
    for h2_link in h1_data['h2_links']:
        # 构建完整的URL（如果h2_link是相对路径）
        if not h2_link.startswith('http'):
            full_link = f'https://www.zysj.com.cn{h2_link}'
        else:
            full_link = h2_link
        try:
            # 发送HTTP请求获取h2页面内容
            response = requests.get(full_link)
            response.raise_for_status()  # 如果请求失败，抛出HTTPError异常
            response.encoding = 'utf-8'

            # 解析h2页面内容
            soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')

            # 提取所有li标签的内容
            for li_tag in soup.find_all('li'):
                # 创建一个字典来存储title和link
                item = {}
                if li_tag.a and 'title' in li_tag.a.attrs:
                    item['title'] = li_tag.a['title']
                if li_tag.a and 'href' in li_tag.a.attrs:
                    item['h3_link'] = li_tag.a['href']
                if item:  # 只有当item不为空时才添加到列表中
                    h2_data.append(item)

        except requests.RequestException as e:
            print(f"请求{full_link}时出错: {e}")
            continue  # 继续处理下一个链接

# 将h2_data保存为h2.json文件
with open('h2.json', 'w', encoding='utf-8') as file:
    json.dump(h2_data, file, ensure_ascii=False, indent=4)

print('h2页面中的li标签内容已保存为h2.json文件。')
