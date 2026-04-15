from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage


# 初始化模型
chat = ChatTongyi(model='qwen3-max', temperature=0.7)

# 构建对话消息
messages = [
    SystemMessage(content="你是一名来自边塞的诗人。"),
    HumanMessage(content="请给我写一首唐诗"),
    AIMessage(content="锄禾日当午，汗滴禾下土。谁知盘中餐，粒粒皆辛苦。"),
    HumanMessage(content="给予你上一首的格式，再来一首宋词吧")
]

# 调用模型进行对话，流式输出
for chunk in chat.stream(messages):
    if hasattr(chunk, "content") and chunk.content:
        print(chunk.content, end=" ", flush=True)






