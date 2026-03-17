

import requests  
from bs4 import BeautifulSoup  
import csv  
import os
  
# 发送HTTP请求  
url = 'https://www.zysj.com.cn/lilunshuji/zhenjiuxue/index.html'  # 要爬取的页面  
response = requests.get(url)  
response.encoding = 'utf-8'
response.raise_for_status()  # 如果请求失败，则抛出异常  
  
# 解析HTML  
soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')
  
# 取数据    
entries = []  
for li in soup.find_all('li', id=lambda x: x and x.startswith('si')):  # 使用lambda来匹配以'si'开头的id  
    title_a = li.find('a', title=True)  # 查找具有title属性的<a>标签  
    if title_a:  
        title = title_a.text.strip()  # 提取标题  
        href = title_a['href']  # 提取链接  
        entries.append((title, href))  # 添加到列表中  
  
# 保存为CSV  
with open('名称.csv', 'w', newline='', encoding='utf-8') as csvfile:  
    fieldnames = ['穴位、经脉、常见病症名称', 'H1_Link']  # CSV的列名  
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)  
  
    writer.writeheader()  # 写入表头  
    for entry in entries:  
        writer.writerow({'穴位、经脉、常见病症名称': entry[0],'H1_Link': entry[1]})  # 写入数据  

 
  
# 保存为CSV，指定新的保存路径  
# 设定新的目录路径  
new_directory = "E:\\爬虫学习\\中医问答爬虫"  # 确保目录存在，否则可能需要创建它  
if not os.path.exists(new_directory):  
    os.makedirs(new_directory)  # 创建目录（如果它不存在）  
  
# 构造完整的文件路径  
csv_file_path = os.path.join(new_directory, '穴位、经脉名称常见病症名称.csv')  
  
# 保存数据到CSV文件  
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:  
    fieldnames = ['穴位、经脉、常见病症名称', 'H1_Link']  # CSV的列名  
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)  
  
    writer.writeheader()  # 写入表头  
    for entry in entries:  
        writer.writerow({'穴位、经脉、常见病症名称': entry[0], 'H1_Link': entry[1]})  # 写入数据  
  
# 打印数据保存成功的信息以及文件保存的路径  
print("数据已保存为CSV文件。")  
print("文件被保存在：", csv_file_path)  # 使用csv_file_path变量来打印文件路径