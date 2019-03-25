counts=['a','b','c','a']
a = list()
[a.append(i) for i in counts if a.count(i)==0]
print(a)