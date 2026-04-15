from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import os

# 更简洁的模板用法
prompt = PromptTemplate.from_template(
    "我的邻居姓{lastname}, 刚生了{gender}, 帮忙起名字,请简略回答。"
)

# 直接传入变量，让 langchain 自动处理
model = ChatOpenAI(
    model="kimi-k2.5",
    api_key=os.getenv("CODING_API_KEY") or os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://coding.dashscope.aliyuncs.com/v1"
)

# 链式调用，更简洁
chain = prompt | model

# 流式输出
for chunk in chain.stream({"lastname": "林", "gender": "女"}):
    print(chunk.content, end="", flush=True)

print()