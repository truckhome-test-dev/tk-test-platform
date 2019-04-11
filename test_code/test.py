# counts=['a','b','c','a']
# a = list()
# [a.append(i) for i in counts if a.count(i)==0]
# print(a)
with open("a.txt","r",encoding="utf-8") as f:
    lines = f.readlines()
    #print(lines)
with open("a.txt","w",encoding="utf-8") as f_w:
    for line in lines:
        print (1)
        break