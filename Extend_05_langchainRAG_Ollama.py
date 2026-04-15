from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage


# 初始化模型
# chat = ChatOllama(model='llama3.2:3b', temperature=0.7)
chat = ChatOllama(model='qwen2.5:1.5b', temperature=0.7)

# 构建对话消息
messages = [
    SystemMessage(content="你是一名充满浪漫主义色彩的诗人。"),
    HumanMessage(content="请给我写一首唐诗"),
    AIMessage(content="飞流直下三千尺，疑是银河落九天。"),
    HumanMessage(content="给予你上一首的格式，再来一首宋词吧")
]

# 调用模型进行对话，流式输出
for chunk in chat.stream(messages):
    if hasattr(chunk, "content") and chunk.content:
        print(chunk.content, end=" ", flush=True)



