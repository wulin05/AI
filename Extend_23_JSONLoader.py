"""
JSONLoader用于将JSON数据加载为Document类型的对象
使用JSONLoader需要额外安装: pip install jq

jq是一个跨平台的json解析工具, LangChain底层对JSON的解析就是基于jq工具实现的,意思就是说langchain的JSONLoader需要jq才能正常工作.
即, 将JSON数据的信息抽取出来, 封装为Document对象,抽取的时候依赖jq_schema语法

{
    "name": "周杰伦",
    "age": 11,
    "hobby": ["唱", "跳", "RAP"],
    "other":{
        "addr": "深圳",
        "tel": "1233213344"
    }
}

. 表示整个JSON对象(根)
[]表示数组
.name表示抽取周杰伦
.hobby表示抽取爱好数组
.hobby[1]或.hobby.[1]表示抽取爱好数组中的第二个元素,即跳
.other.addr表示抽取地址深圳

[
    {"name": "周杰伦", "age": 11, "gender": "男"},
    {"name": "蔡依林", "age": 12, "gender": "女"},
    {"name": "王力宏", "age": 13, "gender": "男"},
]

.[].得到3个字典
.[].name表示抽取全部的name,即得到3个name信息

"""

from langchain_community.document_loaders import JSONLoader


# loader = JSONLoader(
#     file_path="./data/stu.json",   # 必填
#     # jq_schema=".other.addr",      # 必填,想抽取的内容,所以,如果是.other.addr，得到的就是是字符串,那么text_content可以不用,因为默认是True.
#     jq_schema=".",      # 必填,jq的解析语法: 想抽取整个文件内容,即得到一个字典(就不是字符串了),所以下面的text_content=False才有意义,如果jq_schema="."但text_content=True,则得到的就是字符串形式的整个JSON文本
#     text_content=False,     # 抽取的是否是字符串,默认是True
#     # json_lines=True,        # 是否是JsonLines文件(即,每一行都是JSON文件),默认是False
# )


# loader = JSONLoader(
#     file_path="./data/stus.json",   # 必填
#     jq_schema=".[].name",      # 必填,jq的解析语法: 想抽取所有name相关value
#     text_content=False,     # 抽取的是否是字符串,默认是True
#     # json_lines=True,        # 是否是JsonLines文件(即,每一行都是JSON文件),默认是False
# )

loader = JSONLoader(
    file_path="./data/stu_json_lines.json",   # 必填
    jq_schema=".name",      # 必填,jq的解析语法: 想抽取所有name相关value
    text_content=False,     # 抽取的是否是字符串,默认是True
    json_lines=True,        # 是否是JsonLines文件(即,每一行都是独立的标准JSON),默认是False
)

doc = loader.load()
print(doc)



"""
如下是一个典型的JsonLines文件
{"name": "周杰伦", "age": 11, "gender": "男"}
{"name": "蔡依林", "age": 12, "gender": "女"}
{"name": "王力宏", "age": 13, "gender": "男"}

"""