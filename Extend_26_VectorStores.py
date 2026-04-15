from chromadb import Documents
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
# from langchain_community.vectorstores import ChromaVectorStore
from langchain_community.document_loaders import CSVLoader


"""
1. 内置向量存储的使用示例：
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DashScopeEmbeddings

vector_store = InMemoryVectorStore(embedding=DashScopeEmbeddings())

# 添加文档到向量存储,并指定id
vector_store.add_documents(
    documents=[doc1, doc2],
    ids=["id1", "id2"],
)

# 删除文档(通过指定的id删除)
vector_store.delete(ids=["id1"])

# 相似性搜索
similar_docs = vector_store.similarity_search(query="hello", k=1)

"""


"""
2. 外部(Chroma)向量存储的使用示例：
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings

# vector_store = Chroma(
#     collection=Chroma(collection_name="my_collection", embedding_function=DashScopeEmbeddings(),persist_directory="./chroma_langchain_db")
# )

# 这是示例代码,如果你想使用Chroma向量存储,需要先安装chroma库,并且需要在本地运行chroma服务,然后才能使用Chroma向量存储,具体的安装和使用方法可以参考chroma的官方文档 
vector_store = Chroma(
    collection_name="my_collection",
    embedding_function=DashScopeEmbeddings(),
    persist_directory="./chroma_langchain_db"
)

"""

# 创建向量存储实例
vector_store = InMemoryVectorStore(embedding=DashScopeEmbeddings())
# vectorstore.add_texts(["hello world", "hi there", "how are you"], metadata=[{"source": "1"}, {"source": "2"}, {"source": "3"}])
# print(vectorstore.similarity_search("hello", k=1))

# 加载CSV文件,后续把其中的文本数据添加到向量存储中
loader = CSVLoader(
    file_path="./data/info.csv", 
    # csv_args={
    #     "delimiter": "," ,     # 指定分隔符
    #     # "delimiter": "|",    # 指定分隔符
    #     # "quotechar": '"',      # 表示""里面的字符不作为分隔符
    #     # "fieldnames": ['a', 'b', 'c', 'd']  # 这个是说用这些字符当表头
    # },
    encoding="utf-8",
    source_column="nation"   # 指定哪个列作为metadata中的source信息,如果不指定,则默认是source_column=None,即不把任何列作为metadata中的source信息    
)

Documents = loader.load()
# print(Documents[1])

# 添加文档到向量存储,并指定id
vector_store.add_documents(
    Documents,
    ids=["id"+str(i) for i in range(1, len(Documents)+1)]
)

# 删除文档(通过指定的id删除)
vector_store.delete(ids=["id1", "id2"])

# 相似性搜索,返回的结果类型是list[Document],每个Document对象的page_content属性是文本内容,metadata属性是一个字典,包含了source信息
similar_docs = vector_store.similarity_search(
    query="找出商人的相关信息", 
    k=2      # 检索的结果要几个
)

print(similar_docs)