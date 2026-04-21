from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_openai import ChatOpenAI
import os

# str_parser 是将 AIMessage 类对象转换成 str
str_parser = StrOutputParser()

# json_parser 是将 AIMessage 类对象转换成字典 dict
# json_parser = JsonOutputParser()

# 不用上面的json_parser的解析器了,用自定义lambda函数
my_func = RunnableLambda(lambda ai_msg: {"name": ai_msg})

model = ChatOpenAI(
    model="qwen3-max",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"

    # model="kimi-k2.5",
    # api_key=os.getenv("CODING_API_KEY"),
    # base_url="https://coding.dashscope.aliyuncs.com/v1"
)

frist_prompt = PromptTemplate.from_template(
    "我的邻居姓: {lastname}, 刚生了{gender}, 帮忙起两个名字,仅告诉我名字即可,不要额外信息"
)

second_prompt = PromptTemplate.from_template(
    "姓名{name},请帮我解析名字的含义,不要其他跟这个名字无关的信息。"
)

chain = frist_prompt | model | my_func | second_prompt | model | str_parser
"""
# 也可以直接将lambda函数加入链: 因为Runnable接口类再实现__or__的时候,支持Callable接口的实例:
chain = frist_prompt | model | (lambda ai_msg: {"name": ai_msg}) | second_prompt | model | str_parser
# 等价于: 因为LangChain中对右边的加入的链会判断是否是Runnable对象,如果不是,会用RunnableLambda()包装
chain = frist_prompt | model | RunnableLambda(lambda ai_msg: {"name": ai_msg}) | second_prompt | model | str_parser


def __or__(
    self,
    other: Runnable[Any, Other]
    | Callable[[Iterator[Any]], Iterator[Other]]
    | Callable[[AsyncIterator[Any]], AsyncIterator[Other]]
    | Callable[[Any],[Other]]
    | Mapping[str, Runnable[Any, Other] | Callable[[Any], Other] | Any],
) -> RunnableSerializable[Input, Other]:

如上述代码示例, | 符号(底层是调用__or__)组链, 是支持函数加入的。
其本质是将函数自动转换为 RunnableLambda

"""

# 建议使用流式输出
for chunk in chain.stream({"lastname": "林", "gender": "女孩"}):
    print(chunk, end="", flush=True)