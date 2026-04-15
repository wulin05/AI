from langchain_community.embeddings import DashScopeEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# 初始化模型
model = DashScopeEmbeddings(model="text-embedding-v2")

# 生成向量
vec1 = model.embed_query("我喜欢你")
vec2 = model.embed_query("我对你有好感")
vec3 = model.embed_query("今天天气不错")

# ========== 查看向量维度 ==========
print("=" * 50)
print("【向量维度展示】")
print("=" * 50)
print(f"vec1 类型：{type(vec1)}")
print(f"vec1 维度：{len(vec1)}")
print(f"vec1 前10个元素：{vec1[:10]}")
print()

# ========== 查看相似度矩阵结构 ==========
print("=" * 50)
print("【相似度矩阵展示】")
print("=" * 50)

# 把三个向量一起传入，生成 3x3 的相似度矩阵
all_vecs = [vec1, vec2, vec3]
sim_matrix = cosine_similarity(all_vecs)

print(f"相似度矩阵形状：{sim_matrix.shape}")
print(f"\n完整相似度矩阵:")
print(sim_matrix)
print()

# ========== 演示不同索引的访问 ==========
print("=" * 50)
print("【不同索引访问演示】")
print("=" * 50)
print(f"sim_matrix[0][0] = {sim_matrix[0][0]:.4f}  (vec1 vs vec1)")
print(f"sim_matrix[0][1] = {sim_matrix[0][1]:.4f}  (vec1 vs vec2)")
print(f"sim_matrix[0][2] = {sim_matrix[0][2]:.4f}  (vec1 vs vec3)")
print(f"sim_matrix[1][2] = {sim_matrix[1][2]:.4f}  (vec2 vs vec3)")
print(f"sim_matrix[2][1] = {sim_matrix[2][1]:.4f}  (vec3 vs vec2)")
print()

# ========== 原来的输出 ==========
print("=" * 50)
print("【原始输出】")
print("=" * 50)
print(f"'我喜欢你' vs '我对你有好感': {sim_matrix[0][1]:.4f}")
print(f"'我喜欢你' vs '今天天气不错': {sim_matrix[0][2]:.4f}")
