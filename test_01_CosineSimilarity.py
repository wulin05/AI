from langchain_community.embeddings import DashScopeEmbeddings
from sklearn.metrics.pairwise import cosine_similarity  # type: ignore

# 初始化模型: text-embedding-v2是阿里的一种向量模型
model = DashScopeEmbeddings(model="text-embedding-v2")

# 生成向量
vec1 = model.embed_query("我喜欢你")
vec2 = model.embed_query("我对你有好感")
vec3 = model.embed_query("今天天气不错")

# 计算相似度
sim_12 = cosine_similarity([vec1], [vec2])[0][0]
sim_13 = cosine_similarity([vec1], [vec3])[0][0]

"""
sim_12 = cosine_similarity([vec1], [vec2])
print(f"{sim_12}") # sim_12是一个2维数组[[0.xxx]],更确切的说,是一个1x1的相似度矩阵, 需要通过[0][0]来访问其中的值。

"""

print(f"'我喜欢你' vs '我对你有好感': {sim_12:.4f}")
print(f"'我喜欢你' vs '今天天气不错': {sim_13:.4f}")


# 上面的其实也可以这样写：
"""
结果是：(m, n)的相似度矩阵, 如下：
       vec2        vec3
vec1   0.xxx       0.xxx
"""
sim_1_23 = cosine_similarity([vec1], [vec2, vec3])
print(f"'我喜欢你' vs '我对你有好感': {sim_1_23[0][0]:.4f}")
print(f"'我喜欢你' vs '今天天气不错': {sim_1_23[0][1]:.4f}")


print("\n" + "=" * 50)


"""
cosine_similarity([vec1, vec2], [vec3])是生成一个2x1的相似度矩阵，第一行是vec1和vec3的相似度，第二行是vec2和vec3的相似度。
结果是(m x n)的相似度数组, 如下：
       vec3
vec1   0.xxx
vec2   0.xxx
"""
sim_1_3 = cosine_similarity([vec1, vec2], [vec3])[0][0]
print(f"'我喜欢你' vs '今天天气不错': {sim_1_3:.4f}")

sim_2_3 = cosine_similarity([vec1, vec2], [vec3])[1][0]
print(f"'我对你有好感' vs '今天天气不错': {sim_2_3:.4f}")


