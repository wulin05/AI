from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage


# 初始化模型
chat = ChatTongyi(model='qwen1.5-110b-chat', temperature=0.7)

# 构建对话消息,就不需要HumanMessage,SystemMessage,AIMessage
messages = [
    ("system", "你是一名来自边塞的诗人。"),
    ("human", "请给我写一首唐诗"),
    ("ai", "飞流直下三千尺，疑是银河落九天。"),
    ("human", "给予你上一首的格式，再来一首宋词吧")
]

# 调用模型进行对话，流式输出
for chunk in chat.stream(messages):
    if hasattr(chunk, "content") and chunk.content:
        print(chunk.content, end=" ", flush=True)






