from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_openai import ChatOpenAI
import os

# model = ChatTongyi(model="qwen3-max")
model = ChatOpenAI(
    model="kimi-k2.5",
    api_key=os.getenv("CODING_API_KEY") or os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://coding.dashscope.aliyuncs.com/v1"   
)

prompt = PromptTemplate.from_template(
    "我的邻居姓{lastname}, 刚生了{gender}, 帮忙起名字,请简略回答。"
)

# 创建StrOutputParser解析器,本身它是runnable的接口子类,所以既可以将AIMessage对象字符串化,又可以加入chain链~
parse = StrOutputParser()

"""
chain = prompt | model | model  
这样使用会报错, 因为model的输出是AIMessage类对象,而model的输入类型不包括这个类型,所以报错如下: 
ValueError: Invalid input type <class 'langchain_core.messages.ai.AIMessage'>. Must be a PromptValue, str, or list of BaseMessages.
"""
chain = prompt | model | parse | model | parse

res = chain.invoke({"lastname": "林", "gender": "女孩"})

# 如果没有最后的parse的解析器的话,res的类型是AIMessage类型,所以需要用.content来得到确切的回复.如果再用上parse的话,那直接打印res就可以了
# print(res.content)  # 反而会报错：AttributeError: 'TextAccessor' object has no attribute 'content'
print(res)