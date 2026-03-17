import urllib.parse
import re

# 读取文件内容
file_path = r"teacher.ttl"
with open(file_path, 'r', encoding='utf-8') as file:
    ttl_content = file.read()

# 定义替换函数
def decode_uri(match):
    encoded_uri = match.group(1)
    decoded_part = urllib.parse.unquote(encoded_uri, encoding='utf-8')
    return f'annotations:{decoded_part}'

# 使用正则表达式进行替换
# 这个正则表达式匹配类似 <ann:%E4%B8%89%E7%88%AA%E9%BE%99> 的字符串
ttl_content = re.sub(r'ann:([^>]+)', decode_uri, ttl_content)

# 将解码后的内容写入文件
with open(file_path, 'w', encoding='utf-8') as file:
    file.write(ttl_content)

print("URI解码和替换已完成。")
