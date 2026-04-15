from langchain_community.llms.tongyi import Tongyi
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document
from langchain_community.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import FakeEmbeddings
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

# 意图：RAG(检索增强生成) - 先从知识库检索相关信息，再生成回答

# 1. 模拟一个知识库（实际项目中会从文档加载）
documents = [
    Document(page_content="林姓起源于商朝，始祖是比干的儿子林坚。", metadata={"source": "姓氏起源"}),
    Document(page_content="林姓在福建、广东、台湾分布最多。", metadata={"source": "姓氏分布"}),
    Document(page_content="林姓的著名人物有林则徐、林徽因、林青霞等。", metadata={"source": "姓氏名人"})
]

# 2. 创建向量存储和检索器
embeddings = FakeEmbeddings(size=10)
vectorstore = InMemoryVectorStore.from_documents(documents, embeddings)
# 检索器（retriever）返回的是文档列表（list）
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})  # 检索最相关的2条信息

# 3. 提示模板: {context} 会被检索器填充，但 prompt_template 需要的是 {"context": "...", "question": "..."} 这样的字典。
prompt_template = PromptTemplate.from_template(
    """根据以下背景知识回答问题:
    背景知识: {context}
    问题: {question}
    请简略回答。""" 
)

# 格式化函数：将文档列表转换为字符串
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

model = Tongyi(model="qwen-max-2025-01-25")

# 4. 组合成链：检索器 -> 格式化文档 -> 提示模板 -> 模型
chain = (
    RunnablePassthrough.assign(context=retriever | RunnableLambda(format_docs))
    | prompt_template
    | model
)

# # 4. 组合成链: 检索器 -> 提示模板 -> 模型
# chain = retriever | prompt_template | model

# 5. 调用链获取结果(只需传问题,检索器会自动找相关知识)
res = chain.invoke(input={"question": "林姓有什么名人?"})

print(f"chain 结果基于检索的知识回答：{res}")