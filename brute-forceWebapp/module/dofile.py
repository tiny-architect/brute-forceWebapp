#-*-coding:utf-8

def readfile(filename):
    with open(filename,"rb") as f:
        content = [i.strip() for i in f.readlines()]
    return content

def writelog(filename,content):
    with open(filename,"a") as f:
        f.write(content)
        f.write("\n")
    return 0