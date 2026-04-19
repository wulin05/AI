from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.document_loaders import CSVLoader

"""
需要用到Chroma 向量数据库(轻量级的)
确保pip install langchain-chroma, chromadb 这两个库

向量存储类均提供了3个通用API接口:
1. add_documents, 用于添加文档到向量存储中,需要指定文档和对应的id
2. delete, 用于从向量存储中删除文档,需要指定要删除的文档的id
3. similarity_search, 用于在向量存储中进行相似性搜索,需要指定查询文本、返回的相似文档数量k和可选的过滤条件filter

"""

vector_store= Chroma(
    collection_name="my_collection",                # 给当前向量存储起个名字,类似数据库的表名
    embedding_function=DashScopeEmbeddings(),       # 嵌入模型,这里使用DashScopeEmbeddings作为示例,你也可以使用其他的嵌入模型,只要它符合LangChain的嵌入模型接口即可
    persist_directory="./chroma_langchain_db"       # 持久化目录,即向量存储的数据会保存在这个目录下,如果不指定这个参数,则向量存储的数据会保存在内存中,当程序结束时数据会丢失
)

loader = CSVLoader(
    file_path="./data/info.csv",
    encoding="utf-8",
    source_column="nation"
)

Documents = loader.load()


# 注释掉的这部分内容,因为向量存储的数据已经保存在persist_directory指定的目录下了,所以不需要每次都添加文档到向量存储了,只需要在第一次运行时添加一次文档到向量存储就可以了,后续的运行只需要进行相似性搜索就可以了
# 添加文档到向量存储,并指定id
vector_store.add_documents(
    Documents, 
    ids=["id"+str(i) for i in range(1, len(Documents)+1)]
)

# # 删除文档(通过指定的id删除)
# vector_store.delete(ids=["id1", "id2"])

# 相似性搜索
similar_docs = vector_store.similarity_search(
    query="谁是歌手呀？", 
    k=1,
    filter={"source": "台湾"}    # 这个filter参数表示在进行相似性搜索时,只考虑metadata中source字段的值为"台湾"的文档,如果不指定这个参数,则表示不进行过滤,即考虑所有文档
)

print(similar_docs)   # 打印相似性搜索的结果,得到一个列表,里面有多个Document对象,每个Document对象的page_content属性就是一个文本字符串形式的文档内容,每个Document对象的metadata属性就是一个字典形式的元数据信息