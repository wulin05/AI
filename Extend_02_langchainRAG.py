"""
RAG 的全称是 Retrieval-Augmented Generation,译为检索增强生成。

它是一种结合信息检索与大语言模型生成的技术框架：先根据用户问题从知识库中检索相关文档，
再将这些文档作为“参考资料”连同问题一起交给模型生成更准确、更有时效性的回答。

"""

from langchain_community.llms.tongyi import Tongyi
import os
"""
RAG: Retrieval Augmented Generation
检索增强生成技术，利用检索外部文档提升生成结果质量
"""

llm = Tongyi(model='qwen-max', temperature=0.7)

# res = llm.invoke("帮我讲个笑话吧")
# print(res)

res = llm.stream("给我讲个笑话吧")
for chunk in res:
    # if hasattr(chunk, "content") and chunk.content:
    #     print(chunk.content, end="", flush=True)
    print(chunk, end=" ", flush=True)
print()

