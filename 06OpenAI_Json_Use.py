import json

"""
json对象 => Python字典
Json数组 => Python列表内含多个字典
"""

# d是Python字典
d = {"name": "周杰伦", "age": 30, "gender": "男"}
print(str(d))

# 将Python字典转换为json字符串
s = json.dumps(d, ensure_ascii=False)
print(s)

# l是Python列表，内含多个字典
l = [
    {"name": "周杰伦", "age": 30, "gender": "男"},
    {"name": "林俊杰", "age": 28, "gender": "男"},
    {"name": "蔡依林", "age": 29, "gender": "女"},
]

# 将Python列表内的字典对象转换为json数组
print(json.dumps(l, ensure_ascii=False, indent=4))


'''
将json字符串转换为Python字典
也可以说就是字符串转化为Python对象
'''
# json_str是json字符串, json_arr_str是json数组字符串
json_str = '{"name": "周杰伦", "age": 30, "gender": "男"}'
json_arr_str = '[{"name": "周杰伦", "age": 30, "gender": "男"}, {"name": "林俊杰", "age": 28, "gender": "男"},{"name": "蔡依林", "age": 28, "gender": "女"}]'

# 将json字符串转换为Python字典,以及将json数组字符串转换为Python列表
res_dict = json.loads(json_str)
print(res_dict, type(res_dict))

res_list = json.loads(json_arr_str)
print(res_list, type(res_list))

