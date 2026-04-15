"""
chain链的使用
"""
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain_openai import ChatOpenAI
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.runnables import RunnableSerializable

# 创建聊天提示词模板
chat_prompt = ChatPromptTemplate.from_messages(
        [
        ("system", "你是一个浪漫诗人,可以天马行空作诗"),
        MessagesPlaceholder("history"),
        ("human", "请再来一首宋词:"),
    ]
)

history_data = [
    ("human", "你来写一首宋词"),
    ("ai", "明月几时有？把酒问青天。不知天上宫阙，今夕是何年。我欲乘风归去，又恐琼楼玉宇，高处不胜寒。起舞弄清影，何似在人间。转朱阁，低绮户，照无眠。不应有恨，何事长向别时圆？人有悲欢离合，月有阴晴圆缺，此事古难全。但愿人长久，千里共婵娟。"),
    ("human", "好词，再来一首"),
    ("ai", """东风夜放花千树，更吹落，星如雨。
        宝马雕车香满路。
        凤箫声动，玉壶光转，一夜鱼龙舞。
        蛾儿雪柳黄金缕，笑语盈盈暗香去。
        众里寻他千百度，
        蓦然回首，那人却在，灯火阑珊处。
    """)
]

# 创建模型实例
model = ChatTongyi(
    model="qwen3-max",
    temperature = 0.7,
)

# 返回值chain对象是RunnableSerializable对象： 这个对象是Runnable接口的直接子类,也是大多数组件的父类
chain: RunnableSerializable = chat_prompt | model
print(type(chain))

# try:
#     # Runnable接口,invoke执行
#     response = chain.invoke({"history": history_data})

#     # 安全检查
#     if hasattr(response, 'content') and response.content:
#         print(f"✅ AI 回答：{response.content}")
#     else:
#         print(f"⚠️ 响应异常：{response}")

# except Exception as e:
#     print(f"❌ 错误：{type(e).__name__} - {e}")

# Runnable接口,stream执行
response = chain.stream({"history": history_data})

result = ""
for chunk in response:
    if hasattr(chunk, "content") and chunk.content:
        print(chunk.content, end="", flush=True)
        result += chunk.content    # result用来存储结果,这样如果后续需要用的时候直接可以使用。


