import json
import requests
from bs4 import BeautifulSoup

# 读取h2.json文件
with open('E:\\爬虫学习\\中医问答爬虫\\h2_C完整清洗.json', 'r', encoding='utf-8') as f:
    h2_data = json.load(f)

# 准备一个空列表来存储h3页面的数据
h3_data = []

# 遍历h2_data中的每个条目
for entry in h2_data:
    base_url = 'https://www.zysj.com.cn'
    h3_link = entry['h3_link']
    full_url = base_url + h3_link
    
    try:
        response = requests.get(full_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser', from_encoding='gbk')
            data = {}
            data['title'] = soup.find('h1').text if soup.find('h1') else "标题未找到"
            for item in soup.find_all('div', class_='item'):
                item_name = item.find('div', class_='item-name').text if item.find('div', class_='item-name') else "名称未找到"
                p_tag = item.find('p')
                item_content = p_tag.text if p_tag else None
                data[item_name] = item_content
            h3_data.append(data)
        else:
            print(f"无法获取页面：{full_url} (状态码：{response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"请求出错：{e}")

# 将h3_data列表保存到h3.json文件中
with open('h3_C完整.json', 'w', encoding='utf-8') as f:
    json.dump(h3_data, f, ensure_ascii=False, indent=4)

print('已保存为h3_C完整.json文件。')
