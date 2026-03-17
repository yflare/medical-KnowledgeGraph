import requests  
import json  
from bs4 import BeautifulSoup  
  
# 读取h1.json文件，获取h2页面链接列表  
with open('part1/穴位、经脉、常见病症名称.json', 'r', encoding='utf-8') as file:  
    h1_data = json.load(file)  
h2_links = [item['H1_Link'] for item in h1_data if 'H1_Link' in item]  # 假设H1_Link是包含h2链接的键  

# 存储所有h2页面中的<p>标签内容  
h2_p_contents = []  
  
# 遍历h2链接，发送请求，提取<p>标签内容  
base_url = 'https://www.zysj.com.cn'  # 完整的网站域名  
for link in h2_links:  
    full_link = f"{base_url}{link}"  # 构建完整的URL  
    response = requests.get(full_link)  
    response.raise_for_status()  
    soup = BeautifulSoup(response.content, 'html.parser', from_encoding='gbk')  # 如果网页使用的是GBK编码
      
    # 提取所有<p>标签内容  
    p_tags = soup.find_all('p')  
    p_contents = [p.get_text(strip=True) for p in p_tags]  # 获取<p>标签的纯文本内容，并去除首尾空白字符  
      
    # 将h2页面的URL和对应的<p>标签内容存储到一个字典中  
    h2_page_data = {'h2_link': link, 'p_contents': p_contents}  
    h2_p_contents.append(h2_page_data)  
  
# 保存提取到的<p>标签内容到新的JSON文件  
with open('h2_p_contents.json', 'w', encoding='utf-8') as file:  
    json.dump(h2_p_contents, file, ensure_ascii=False, indent=4)  
  
print("h2页面中的<p>标签内容已保存为h2_p_contents.json文件。")