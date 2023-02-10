

# coding:utf-8
import os

# 指定文件夹
folder_name = r"D:\VS2019Project\PDF\著作权\code"

# 创建文件
f = open(folder_name+"\output.txt", 'w+')

# 遍历文件夹下所有.py文件
for root, dirs, files in os.walk(folder_name):
    for file in files:
        if os.path.splitext(file)[1] == '.py':
            with open(os.path.join(root, file), 'r', encoding='utf-8') as f1:
                f.write(file+'\n')
                f.write(f1.read())
                # f.write('\n\n')

# 关闭文件
f.close()