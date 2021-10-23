from mdutils.mdutils import MdUtils




mdFile = MdUtils(file_name="Example_Markdown_02")

#文章头部信息
mdFile.write("---\n")
mdFile.write("title: '最大的比特币矿池封锁了来自中国大陆的互联网接入' \n")
mdFile.write("date: '2021-10-14 11:24:00' \n")
mdFile.write("tags: ['蚂蚁矿机'] \n")
mdFile.write("draft: false \n")
mdFile.write("summary: '随着中国禁止与加密货币有关的活动的步伐，Antpool正在封锁中国大陆IP地址的用户。'\n")
mdFile.write("---\n")

#文章内容


mdFile.create_md_file()

#最后处理文件，删除文件前3行,否则网站解析md出错
with open('Example_Markdown_02.md', 'r',encoding='UTF-8') as fin:
    data = fin.read().splitlines(True)
with open('Example_Markdown_02.md', 'w',encoding='UTF-8') as fout:
    fout.writelines(data[3:])
