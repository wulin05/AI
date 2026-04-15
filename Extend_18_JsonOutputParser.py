from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_openai import ChatOpenAI
import os

# str_parser 是将 AIMessage 类对象转换成 str
str_parser = StrOutputParser()
# json_parser 是将 AIMessage 类对象转换成字典 dict
json_parser = JsonOutputParser()

model = ChatOpenAI(
    model="qwen3-max",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # base_url="https://coding.dashscope.aliyuncs.com/v1"
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

frist_prompt = PromptTemplate.from_template(
    "我的邻居姓{lastname}, 刚生了{gender}, 帮忙起名字，并封装到 JSON 格式返回给我。"
    "要求 key 是 name, value 就是起的名字。请严格遵守格式要求。"
)

second_prompt = PromptTemplate.from_template(
    "姓名{name},请帮我解析含义。"
)

chain = frist_prompt | model | json_parser | second_prompt | model | str_parser

# res: str = chain.invoke({"lastname": "林", "gender": "女孩"})

# print(res, "/n", type(res))

# 建议使用流式输出
for chunk in chain.stream({"lastname": "林", "gender": "女孩"}):
    print(chunk, end="", flush=True)