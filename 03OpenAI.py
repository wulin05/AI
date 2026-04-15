# OpenAI库的流式输出
from openai import OpenAI
import os

# api_key = os.getenv("CODING_API_KEY") or os.getenv("DASHSCOPE_API_KEY")
# if not api_key:
#     raise RuntimeError(
#         "Missing API key. Set CODING_API_KEY (preferred) or DASHSCOPE_API_KEY."
#     )

# 1. 获取client对象：OpenAI类对象
client = OpenAI(
    api_key=os.getenv("CODING_API_KEY"),  # 直接传入你的环境变量
    base_url="https://coding.dashscope.aliyuncs.com/v1",
)

messages = [
        # system角色：设定模型的行为和规则
        {"role": "system", "content": "你是一个Python编程专家，回答准确而且话非常多"},
        # assistant角色：设定模型的回答，由用户设定
        {"role": "assistant", "content": "好的，我是编程专家，并且话非常多，你要问什么？"},
        # user角色：设定用户的提问
        {"role": "user", "content": "如何安装Python？并输出1~10的代码！"},
]

# 2. 调用模型
response = client.chat.completions.create(
    model="qwen3.5-plus",
    messages=messages,
    stream=True,
)

# 3. 流式输出
for chunk in response:
    delta = chunk.choices[0].delta
    if hasattr(delta, "content") and delta.content:
        # end=""：不换行，每一段之间以空格分隔；flush=True：立即刷新缓冲区,输出内容
        print(delta.content, end="", flush=True) 
