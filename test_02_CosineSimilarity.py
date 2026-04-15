from langchain_community.embeddings import DashScopeEmbeddings
from Extend_01_CosineSimilarity import cosine_similarity


# 初始化模型
model = DashScopeEmbeddings(model="text-embedding-v2")
# model = DashScopeEmbeddings()

# 生成向量
vec1 = model.embed_query("我喜欢你")
vec2 = model.embed_query("我对你有好感")
vec3 = model.embed_query("今天天气不错")

# 计算相似度
sim_12 = cosine_similarity(vec1, vec2)
sim_13 = cosine_similarity(vec1, vec3)

print(f"'我喜欢你' vs '我对你有好感': {sim_12:.4f}")
print(f"'我喜欢你' vs '今天天气不错': {sim_13:.4f}")

