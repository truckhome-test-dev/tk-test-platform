# counts=['a','b','c','a']
# a = list()
# [a.append(i) for i in counts if a.count(i)==0]
# print(a)
import time
data="2019-05-10 00:00:00 - 2019-06-10 00:00:00"
data=data.split(" - ")
print(data[0],type(data[0]))


start_time = int(time.mktime(time.strptime(data[0], '%Y-%m-%d %H:%M:%S')))
print(start_time)