import re
# s='"url": "https://api.360che.com/comment/submit.aspx"'
# pattern = r'"http\S+"'
#
# l = re.findall(pattern,s)
# print(len(l))
# if len(l)>=1:
#     l=l[0][1:-1]
#     print(l)

# with open("url.txt", "r", encoding="utf-8") as f_w:
#     while True:
#         line=f_w.readline()
#         if not line:
#             break
#         # print(line)
#         pattern = r'"url": "\S+"'
#         # pattern = r'"name": "\S+"'
#         # line='"url": "https://api.360che.com/comment/submit.aspx"'
#         l = re.findall(pattern, line)
#         if len(l)>=1:
#             l = l[0][8:-1]
#             print(l)
#
#             # https: // topic
#             # .360
#             # che.com / keyword / getlist.aspx?iden &  a9cc6dcaacb132386ecb6dbca20c2b23"

# test = [[1,2,3,4,5,6],[11,22,33,44,55,66]]
#
# d = {}
# l = []
# for i in test:
#     d['name'] = i[1]
#     d['scor'] = i[2]
#     print(d,id(d))
#     l.append(d)
# print(l)

def logging(level):
    def wrapper(func):
        def inner_wrapper(*args, **kwargs):
            print("[{level}]: enter function {func}()".format(
                level=level,
                func=func.__name__))
            return func(*args, **kwargs)
        return inner_wrapper
    return wrapper

@logging(level='INFO')
def say(something):
    print("say {}!".format(something))

# 如果没有使用@语法，等同于
# say = logging(level='INFO')(say)

@logging(level='DEBUG')
def do(something):
    print("do {}...".format(something))

if __name__ == '__main__':
    say('hello')
    do("my work")