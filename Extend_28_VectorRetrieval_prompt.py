from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
# from langchain_core.messages import Inmemoryvectorstore # 这个是消息类吗？不是，是向量存储类
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DashScopeEmbeddings

import os

"""
提示词: 用户的提问 + 已知的参考资料(从向量库检索得到的文本) -> AI的回答
向量存储的实例,通过add_texts(list[str])方法可以快速添加到向量存储中

流程：
1. 先通过向量存储检索匹配信息
2. 将用户提问和匹配信息一同封装到提示词模板中提问模型

"""

model = ChatOpenAI(
    model="qwen3-max",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# 创建聊天提示词模板
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "以我提供的已知参考资料为主,简洁和专业地回答用户问题,参考资料: {context}."),
        ("user", "用户提问: {input}"),
    ]
)

# 创建向量库实例,也就是向量的存储,这里我们使用官方提供的基于内存的向量库InMemoryVectorStore,它需要一个embedding实例作为参数,我们使用DashScopeEmbeddings这个官方提供的基于达摩思维大模型的文本嵌入模型来生成文本的向量表示。
vector_store = InMemoryVectorStore(embedding=DashScopeEmbeddings(model="text-embedding-v4"))

# 加载数据(向量库的数据) add_texts方法会自动将文本转换成向量并存储到向量库中,所以我们只需要提供文本数据就可以了,不需要自己手动去转换成向量了。
# 前面26,27是add_documents方法,注意看,可以知道它们是通过加载了CSV,JSON,PDF,TEXT的文档来获取文本数据的,而这里我们直接提供文本数据,所以用add_texts方法就可以了。
vector_store.add_texts(
    [
        "减肥就是要少吃多练", 
        "在减肥期间吃东西很重要,清淡少油控制卡路里摄入并运动起来", 
        "跑步是很好的运动",
        "生病期间要多休息,注意保暖,多喝水,吃清淡易消化的食物",
        "感冒了可以吃点感冒药,比如说感冒灵,板蓝根之类的"
    ]
)

input = "关于减肥"

#检索向量库,similarity_search检索相似度最高的k=2，也就是2个文本数据.
result = vector_store.similarity_search(input, k=2)  # 这里的k表示返回最相似的前几个结果,默认是4    
# print(result)

# 上面直接打印result会得到一个list[Document]的结果,其中Document是官方提供的一个类,它有一个page_content属性就是文本内容,
# 但是不好看,所以我们可以把它们拼接成一个字符串,这样便于查看检索结果。
reference_text = "以下是相似度检索到的: [\n"
for doc in result:
    reference_text += doc.page_content + "\n"
reference_text += "]"
# print(reference_text)

# 将聊天提示词模板在链中调用model之前,先打印出内容,查看提示词内容。
def print_prompt(prompt):
    print(prompt.to_string()) 
    print("="*20)
    return prompt

chain = prompt | print_prompt | model | StrOutputParser()

# 调用链,传入用户输入和检索到的参考资料,得到AI的回答
res = chain.invoke({"input": "怎么减肥", "context": reference_text})

print(res)


