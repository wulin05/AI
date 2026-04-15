from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
import os

def print_prompt(full_prompt):
    print("="*20, full_prompt.to_string(), "="*15)
    return full_prompt

# prompt = PromptTemplate.from_template(
#     "你需要根据对话历史回应用户问题。对话历史:" \
#     "{chat_history}。用户当前输入: {input}, 请给出回应。"
# )

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你需要根据对话历史回应用户问题。对话历史: "),
        MessagesPlaceholder("chat_history"),
        ("human", "请回答如下问题：{input}")
    ]
)

str_parser = StrOutputParser()

model = ChatOpenAI(
    # model="kimi-k2.5",
    # api_key=os.getenv("CODING_API_KEY"),
    # base_url="https://coding.dashscope.aliyuncs.com/v1"

    model="qwen3-max",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

bash_chain = prompt | print_prompt | model | str_parser

# 获取指定会话ID的历史会话记录函数
chat_history_store = {}   # 存放多个会话ID所对应的历史会话记录
# 函数传入为会话ID（字符串类型）
# 函数要求返回BaseChatMessageHistory的子类
# BaseChatMessageHistory类专用于存放某个会话的历史记录
# InMemoryChatMessageHistory是官方自带的基于内存存放历史记录的类  
# session_id参数不是自己手动传入的，而是RunnableWithMessageHistory这个“管理器”在内部自动调用这个函数时传进去的。而且从下面的意思来看,就用session_id形参是最合适的！  
def get_history(session_id): 
    if session_id not in chat_history_store:
        # 返回一个新的实例
        chat_history_store[session_id] = InMemoryChatMessageHistory()
    return chat_history_store[session_id]
# def get_history(sid):     
#     if sid not in chat_history_store:
#         # 返回一个新的实例
#         chat_history_store[sid] = InMemoryChatMessageHistory()
#     return chat_history_store[sid]

# 通过RunnableWithMessageHistory获取一个新的带有历史记录功能的chain
conversation_chain = RunnableWithMessageHistory(
    bash_chain,       # 就是上面被附加历史消息的Runnable,核心的业务逻辑链
    get_history,             # 获取指定会话ID的历史会话的函数: 是InMemoryChatMessageHistory的类对象
    input_messages_key="input",      # 声明用户输入消息在模板中的占位符
    history_messages_key="chat_history",   # 声明历史消息在模板中的占位符
    # 如果get_history函数的参数不是session_id,那就要写下面这行代码:
    # history_factory_config=[("sid", "sid")] 
    # 并且不用session_id的话,只能用sid. 这行的意思是：第二个sid是将session_config字典中sid的值(user_001)传给第一个sid(代表get_history参数的sid)。
    # history_factory_config=[("sid", "key_id")]   # 不能用key_id,报错
)


if __name__=='__main__':
    # 如下固定格式,目的: 添加LangChain的配置,为当前程序配置所属的session_id! 如果key用sid的话, get_history函数要用sid形参以及history_factory_config=[("sid", "sid")]要追加这行！！！！
    # session_config = {"configurable": {"sid": "user_001"}}  
    session_config = {"configurable": {"session_id": "user_001"}}

    print(conversation_chain.invoke({"input": "小明有一只猫"}, session_config))
    print(conversation_chain.invoke({"input": "小明有两只狗"}, session_config))
    print(conversation_chain.invoke({"input": "小明共有多少只宠物?"}, session_config))


"""
关于上面的代码,关于session_id的描述,就一句话,不要改这个参数名,改了就要其他地方要跟着改了！！！！
"""
