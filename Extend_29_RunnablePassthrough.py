
import os
from langchain_core.documents import Document

from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.runnables import RunnablePassthrough


"""
28. 向量检索提示词 
把向量检索提示词也加入到链中,让模型在回答问题时,能够参考相似度检索到的文本信息,从而得到更准确的回答。
所以,29的RunnablePassthrough就是为了实现这个功能的。

"""

model = ChatOpenAI(
    model="qwen3-max",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# 创建聊天提示词模板
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "以我提供的已知参考资料为主,简洁和专业地回答用户问题,参考资料: \n{context}."),
        ("user", "用户提问: {input}"),  # 这里的{input}是占位符,它会被我们在调用链时传入的用户输入替换掉
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

input_text = "怎么减肥?"

# 由于上面的InMemoryVectorStore这个类对象,他不是runnable的接口实例,所以我们不能直接把它加入到链中
# 为了让向量库实例能够加入链中,langchain的这个InMemoryVectorStore向量存储对象中提供了一个as_retriever()方法,这个方法会返回一个新的对象,是runnable的接口子类实例对象,它会在链中被调用时,自动调用向量库的相似度检索方法来获取相关文本信息,从而实现了向量检索提示词的功能。
"""
retriever:
可以这么理解：
vector_store = InMemoryVectorStore(...)这个东西的本质是数据库,用来存储向量(问题是: 它不能直接放进chain链中)
as_retriever可以理解为将"数据库"转换成"检索器",这个"检索器"是runnable的接口子类实例对象,它可以放进chain链中,当链被调用时,这个"检索器"会自动调用vector_store的相似度检索方法来获取相关文本信息。
retriever = vector_store.as_retriever(...)

-- 输入：用户的提问 str
retriever.invoke("怎么减肥?")

-- 返回: 向量库的检索结果retriever: list[Document]
[
  Document("减肥就是要少吃多练"),
  Document("清淡少油控制卡路里...")
]

这个检索结果其实是提供给context(提示词模板中的占位符)的,
因此,我们还需要一个自定义format_func函数来把这个返回值retriever是list[Document]的结果格式化成字符串赋值给context,这样才能更好地提供给提示词prompt。

prompt:
  - 输入：用户的提问 str + 向量库的检索结果 dict
  - 输出: 完整的提示词   PromptValue

"""
retriever = vector_store.as_retriever(search_kwargs={"k": 2})  # search_kwargs参数可以用来设置检索的参数,比如这里的k表示返回最相似的前几个结果,默认是4  



# 这个format_func函数就是用来把retriever的输出结果list[Document]格式化成字符串的,这样才能更好地展示在提示词中。
# 其实结果就是: ["减肥就是要少吃多练", "在减肥期间吃东西很重要,清淡少油控制卡路里摄入并运动起来"], 这个是提示词模板中{context}占位符的内容。
def format_func(docs: list[Document]) -> str:
    if not docs:
        return "没有检索到相关信息"
    
    formatted_str = "[\n"
    for doc in docs:
        formatted_str += doc.page_content + "\n"
    formatted_str += "]"
    return formatted_str

# 将聊天提示词模板在链中调用model之前,先打印出内容,确认提示词内容: input和context的内容是否正确。
def print_prompt(prompt):
    print(prompt.to_string()) 
    print("="*20)
    return prompt

# chain
# RunnablePassthrough()这个类的作用是把用户输入的字符串直接传递给提示词模板中的{input}占位符,而不需要我们在调用链时手动去传入一个字典{"input": input_text}这样的参数了,这样就更方便了。
chain = (
    {"input": RunnablePassthrough(), "context": retriever | format_func} | prompt | print_prompt | model | StrOutputParser()
)

"""
注意: 之前是需要invoke()括号内要给两个传入参数: input和context
res = chain.invoke({"input": "怎么减肥", "context": reference_text})
现在由于我们在chain中使用了RunnablePassthrough()这个类,所以我们invoke()括号内只需要给一个参数,
等价于：
res = chain.invoke({"input": "怎么减肥", "context": retriever("怎么减肥")| format_func})
"""
res = chain.invoke(input_text)
print(res)
