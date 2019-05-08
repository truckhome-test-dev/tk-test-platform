import re
# s='"url": "https://api.360che.com/comment/submit.aspx"'
# pattern = r'"http\S+"'
#
# l = re.findall(pattern,s)
# print(len(l))
# if len(l)>=1:
#     l=l[0][1:-1]
#     print(l)

with open("url.txt", "r", encoding="utf-8") as f_w:
    while True:
        line=f_w.readline()
        if not line:
            break
        # print(line)
        pattern = r'"url": "http\S+"'
        # pattern = r'"name": "\S+"'
        # line='"url": "https://api.360che.com/comment/submit.aspx"'
        l = re.findall(pattern, line)
        if len(l)>=1:
            l = l[0][8:-1]
            print(l)