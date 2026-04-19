"""
除了前面 提到的3个Loader以外,还有一个基本的加载器: TextLoader,它是一个非常基础的加载器,可以加载文本文件,并将文本内容封装为Document对象,
它没有特定的解析功能,所以它适用于各种文本格式的文件,包括JSON、CSV、XML等,只要你能将这些文件转换为纯文本格式,就可以使用TextLoader来加载它们.
TextLoader返回仅有一个Document对象的list。

注意, langchain_text_splitters一般是安装了的,如果没有的话,就使用pip install angchain_text_splitters 包即可！
"""
from posixpath import sep

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = TextLoader(
    file_path="./data/test.txt",    # 这个文件虽然是json格式的,但TextLoader会把它当做普通文本来处理,所以它会把整个文件内容作为一个字符串来加载,并封装为一个Document对象
    encoding="utf-8"        # 指定文件的编码格式,windows要写,mac不需要,默认是utf-8
)

# 批量加载.load() -> [Document, Document...]
docs = loader.load()   # 由于TextLoader没有特定的解析功能,所以它会把整个文件内容作为一个字符串来加载,并封装为一个Document对象,所以这里得到的documents是一个列表,里面只有一个Document对象,这个Document对象的page_content属性就是整个文件内容的字符串形式

# print(docs) 

# 正如上面所说,由于TextLoader没有特定的解析功能,所以它会把整个文件内容作为一个字符串来加载,并封装为一个Document对象,所以这里得到的documents是一个列表,里面只有一个Document对象,
# 那么如果这个文件内容太大, 那么可以借助RecursiveCharacterTextSplitter(递归字符文本分割器)来把这个大文本分割成小文本, 主要用于按自然段落分割大文本
splitter = RecursiveCharacterTextSplitter(
    chunk_size=10,     # 表示分割后每个小文本的最大字符数,如果是下面的length_function=lambda x: len(x.split()),那么这个chunk_size就表示分割后每个小文本的最大单词数,默认是1000
    chunk_overlap=0,    # 表示分割后每个小文本之间的重叠部分的长度,默认是0,即没有重叠部分
    # 文本分段依据
    separators=["\n\n", "\n", ".", "。", "!", "?", ",", " ", ""],
    # 字符统计依据
    # length_function=len   # 这个参数表示用来统计文本长度的函数,默认是len函数,即统计文本的字符数,如果你想统计文本的单词数,可以把这个参数设置为lambda x: len(x.split())   
    length_function=lambda x: len(x.split())
)

# 在knowledge_base.py还有split_text(str)的方法,意思就是对传入参数是字符串进行分割
split_docs = splitter.split_documents(docs)   # 这里得到的split_docs是一个列表,里面有多个Document对象,每个Document对象的page_content属性就是一个小文本的字符串形式
# print(split_docs)

for doc in split_docs:
    print(type(doc), doc)