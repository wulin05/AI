import os, json
from langchain_classic.schema import BaseMessage
from langchain_core.messages import message_to_dict, messages_from_dict
from langchain_core.chat_history import BaseChatMessageHistory

# message_to_dict: 单个消息对象(BaseMessage类实例) -> 字典
# messages_from_dict: [字典, 字典...] -> [消息, 消息]
# AIMessage, HumanMessage, SystemMessage 都是 BaseMessage的子类

from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_openai import ChatOpenAI


class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, session_id, storage_path):
        self.session_id = session_id   # 存储会话id
        self.storage_path = storage_path  #不同会话id的存储文件,所在的文件夹路径
        # 完整的文件路径
        self.file_path = os.path.join(self.storage_path, self.session_id)

        # 确保文件夹是存在的
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def add_message(self, message: BaseMessage) -> None:
        # Sequence序列 类似list, tuple(元组)
        all_messages = list(self.messages)    # 已有的消息列表
        # all_messages.extend(message)         # 新的和已有的融合成一个list
        all_messages.append(message)         # 新的和已有的融合成一个list

        # 将数据同步写入到本地文件中
        # 类对象写入文件 -> 一堆二进制
        # 为了方便，可以将BaseMessage消息转为字典(借助json模块以json字符串写入文件)
        # 借助官方message_to_dict: 将单个消息对象(BaseMessage类实例) -> 字典
        # new_messages = []
        # for message in all_messages:
        #     d = message_to_dict(message)
        #     new_messages.append(d)

        # 等价于下面的列表推导式
        new_messages = [message_to_dict(message) for message in all_messages]

        # 将数据写入文件
        with open(self.file_path, "w", encoding="utf-8") as f:
            # 将数据转换成json字符串
            json.dump(new_messages, f)

    @property   # @property装饰器将messages方法变成成员属性,方便后期类对象使用.messages当作成员属性方便使用
    def messages(self) -> list[BaseMessage]:
        # 当前文件内：list[字典], 所以要转换成 list[BaseMessage]
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                messages_data = json.load(f)        # 返回值: list[字典]
                return messages_from_dict(messages_data)  # 需要的是: list[BaseMessage]
        except FileNotFoundError:
            return []
        
    def clear(self) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([], f)


# 就是将前面Extend_20的代码拷贝过来,稍微修改下：
def print_prompt(full_prompt):
    print("="*20, full_prompt.to_string(), "="*15)
    return full_prompt

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你需要根据对话历史回应用户问题。对话历史: "),
        MessagesPlaceholder("chat_history"),
        ("human", "请回答如下问题：{input}")
    ]
)

str_parser = StrOutputParser()

model = ChatOpenAI(

    model="qwen3-max",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

bash_chain = prompt | print_prompt | model | str_parser

# # 获取指定会话ID的历史会话记录函数
# chat_history_store = {}   # 存放多个会话ID所对应的历史会话记录
# def get_history(session_id): 
#     if session_id not in chat_history_store:
#         # 返回一个新的实例
#         chat_history_store[session_id] = InMemoryChatMessageHistory()
#     return chat_history_store[session_id]

# 就将之前的InMemoryChatMessageHistory用下面的文件方式的来读取,进而进行处理....
def get_history(session_id):
    return FileChatMessageHistory(session_id, "./chat_history")


# 通过 RunnableWithMessageHistory() 获取一个新的带有历史记录功能的增强链
conversation_chain = RunnableWithMessageHistory(
    bash_chain,              # 附加历史消息的普通chain
    get_history,             # 获取指定会话ID的历史会话的函数: 这次不是InMemoryChatMessageHistory的类对象了,是
    input_messages_key="input",      # 声明用户输入消息在模板中的占位符
    history_messages_key="chat_history",   # 声明历史消息在模板中的占位符
)


if __name__=='__main__':
    # 如下固定格式,目的: 添加LangChain的配置,为当前程序配置所属的session_id! 如果key用sid的话, get_history函数要用sid形参以及要追加这行history_factory_config=[("sid", "sid")]！！！！
    # session_config = {"configurable": {"sid": "user_001"}}  
    session_config = {"configurable": {"session_id": "user_001"}}

    # print(conversation_chain.invoke({"input": "小明有一只猫"}, session_config))
    # print(conversation_chain.invoke({"input": "小明有两只狗"}, session_config))
    print(conversation_chain.invoke({"input": "小明共有多少只宠物?"}, session_config))