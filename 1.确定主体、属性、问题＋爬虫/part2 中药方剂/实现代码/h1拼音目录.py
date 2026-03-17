import requests  
from bs4 import BeautifulSoup  
import json  
  
# 目标网站的URL  
target_url = 'https://www.zysj.com.cn/zhongyaofang/index.html'  
  
# 发送HTTP请求获取网页内容  
response = requests.get(target_url)  
response.raise_for_status()  # 如果请求失败，抛出HTTPError异常  
response.encoding = 'utf-8'

# 解析网页内容  
soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')
# 存储所有链接的列表  
links = []  
  
# 查找所有的<li>标签，检查是否包含<a>标签并提取href属性  
for li_tag in soup.find_all('li'):  
    a_tag = li_tag.find('a')  
    if a_tag and 'href' in a_tag.attrs:  
        # 构建完整的URL（如果href是相对路径）  
        href = a_tag['href']  
        if not href.startswith('http'):  
            full_link = f'https://www.zysj.com.cn{href}'  
        else:  
            full_link = href  
        links.append(full_link)  
  
# 将链接列表保存为JSON文件  
with open('h1.json', 'w', encoding='utf-8') as file:  
    json.dump(links, file, ensure_ascii=False, indent=4)  
  
print('链接已保存为h1.json文件。')