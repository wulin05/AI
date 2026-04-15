"""
知识库
工具函数的实现

"""
import hashlib
import os
# 将创建的config_data.py文件导入
import config_data as config
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime


def check_md5(md5_str: str):
    """
    检查文件的MD5值是否与预期值匹配
    """
    if not os.path.exists(config.md5_path):
        # if进入表示文件"./md5.text"不存在,那肯定没有处理过这个md5了
        # 使用w模式打开(如果没有该文件,那么w模式就会帮创建),然后直接关闭就行
        open(config.md5_path, 'w', encoding="utf-8").close()
        return False
    else:
        for line in open(config.md5_path, 'r', encoding='utf-8').readlines():
            line = line.strip()    # 处理读取md5文件中的md5值(string类型)的空格和回车
            if line == md5_str:
                return True        # 已处理过
            
        return False    # 代表跑了一圈检查,都没有,说明没有处理过


def save_md5(md5_str):
    """
    将文件的MD5值保存到一个文本文件中
    """
    with open(config.md5_path, 'a', encoding='utf-8') as f:
        f.write(md5_str + '\n')


def get_string_md5(input_str: str, encoding='utf-8'):
    """
    将传入的字符串转化为MD5字符串
    """
    # 将字符串先转换为bytes字节数组
    str_bytes = input_str.encode(encoding=encoding)

    # 创建md5对象
    md5_obj = hashlib.md5()

    md5_obj.update(str_bytes)        # 更新内容(传入即将要转换的字节数组)
    md5_hex = md5_obj.hexdigest()    # 得到md5的十六进制字符串 

    return md5_hex


class KnowledgeBaseService(object):
    def __init__(self):
        # 希望向量数据库文件夹本地不存在时则创建,如果存在则跳过
        os.makedirs(config.persist_directory, exist_ok=True)

        # 创建向量数据库对象实例
        self.chroma = Chroma(
            collection_name=config.collection_name,      #数据库的表名
            embedding_function=DashScopeEmbeddings(model="text-embedding-v4"),
            persist_directory=config.persist_directory   # 数据库本地存储文件夹
        )

        # 文本分割器实例
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,          # 表示分割后每个小文本的最大字符数,如果是下面的length_function=lambda x: len(x.split()),那么这个chunk_size就表示分割后每个小文本的最大单词数,默认是1000
            chunk_overlap=config.chunk_overlap,    # 表示分割后每个小文本之间的重叠部分的长度,默认是0,即没有重叠部分
            # 文本分段依据
            separators=config.separators,          # 自然锻炼划分的符号
            # 字符统计依据
            length_function=len   # 这个参数表示用来统计文本长度的函数,默认是len函数,即统计文本的字符数,如果你想统计文本的单词数,可以把这个参数设置为lambda x: len(x.split())   
            # length_function=lambda x: len(x.split())
        )

    def upload_by_str(self, data:str, filename):
        """
        将传入的字符串,进行向量化,存入向量数据库中
        """
        # 先得到传入字符串的md5值
        md5_hex = get_string_md5(data)

        # 再判断md5值是否存在本地保存的md5值文件中: md5.text
        if check_md5(md5_hex):
            return "[跳过]内容已经存在知识库中"
        
        # 下面表示,如果内容不在知识库里,那么进行处理(是否需要分割),保存到向量数据库中
        # 对传入的文本是否分割进行判断; 在25的py文件中是split_documents(docs)
        if len(data) > config.max_split_char_number:
            knowledge_chunks: list[str] = self.splitter.split_text(data)
        else:
            knowledge_chunks = [data]

        # 将字符串保存到向量数据库中; 在27的py文件中是将文档添加到向量存储中: vector_store.add_documents(...)
        # 另外, 因为下面的add_texts()参数中需要metadata,所以:
        """
        # 根据AI的说法,更安全的写法:
        # 遍历 knowledge_chunks 中的每一个元素（但我们不关心元素内容，所以用 _ 表示忽略），每次都把 metadata 放进新列表中。
        metadatas = [
            {
                "source": filename,
                "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "operator": "啤酒泡泡"
            }
            for _ in knowledge_chunks    
        ]
        """
        metadata = {
            "source": filename,
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator": "啤酒泡泡"
        }
        self.chroma.add_texts(
            # iterable(迭代器),比如数组(list),元组(tuple)都属于迭代器
            knowledge_chunks,
            metadatas = [metadata for _ in knowledge_chunks]
        )

        # 当不在向量数据库的内容存到向量数据库后,那么这时候要将该内容的md5值保存到md5.text中,用于下次如果是相同的内容,就可以根据md5值就不在保存了
        save_md5(md5_hex)

        return "[成功]内容已成功载入向量库"


# ①校验下
if __name__ == '__main__':
    # r1 = get_string_md5("周杰伦")
    # r2 = get_string_md5("周杰伦")
    # r3 = get_string_md5("周杰轮")

    # print(r1)
    # print(r2)
    # print(r3)

    # save_md5("7a8941058aaf4df5147042ce104568da")
    # print(check_md5("7a8941058aaf4df5147042ce104568da"))

    # 上面都是测试代码是否有误,下面真正开始
    service = KnowledgeBaseService()
    r = service.upload_by_str("周杰伦", "testfile")
    print(r)


"""
关于列表推导式的学习：
字符串	[f"Item {i}" for i in range(3)] → ["Item 0", "Item 1", "Item 2"]	
数字	[x*2 for x in [1,2,3]] → [2,4,6]	
字典（新建）	[{"id": i} for i in range(2)] → [{"id":0}, {"id":1}]（每个都是独立对象！）	
已有对象	[obj for _ in range(3)] → [obj, obj, obj]（三个引用指向同一个对象！）⚠️

"""