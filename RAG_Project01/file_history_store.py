import os, json
# from langchain_classic.schema import BaseMessage  # langchain旧版（v0.1 及以前）
from langchain_core.messages import BaseMessage, message_to_dict, messages_from_dict
from langchain_core.chat_history import BaseChatMessageHistory

# print(BaseMessage.__module__)  # 输出: langchain_core.messages,确认包来源是否正确

# 就将之前的InMemoryChatMessageHistory用下面的文件方式的来读取,进而进行处理....
def get_history(session_id):
    return FileChatMessageHistory(session_id, "./chat_history")


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
