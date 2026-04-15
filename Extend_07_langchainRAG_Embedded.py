from langchain_community.embeddings import DashScopeEmbeddings

# 初始化模型
model = DashScopeEmbeddings()

# 不用invoke stream
# embed_query: 单次转换, embed_doucments：批量转换
embedding = model.embed_query("我喜欢你")
embedding_docs = model.embed_documents(["我喜欢你","我稀饭你","今天天气不错"])

# 得到的就是向量
# print(embedding)   
print(f"向量维度：{len(embedding)}")
print(f"向量类型：{type(embedding)}")
print(f"文档向量维度：{len(embedding_docs)}")
print(f"文档向量类型：{type(embedding_docs)}")
print(embedding_docs[0][0])
