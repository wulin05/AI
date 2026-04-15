from openai import OpenAI
import os

client = OpenAI(
    api_key = os.getenv("CODING_API_KEY") or os.getenv("DASHSCOPE_API_KEY") or os.getenv("OPENAI_API_KEY"),
    base_url="https://coding.dashscope.aliyuncs.com/v1",
)

messages = [
    {"role": "system", "content": "你是一个AI助理，回答简洁专业。"},
    {"role": "user", "content": "小米有两条狗，一条叫旺财，一条叫小白。"},
    {"role": "assistant", "content": "好的。"},
    {"role": "user", "content": "大米有3只猫，一只叫花花，一只叫喵喵，一只叫咪咪。"},
    {"role": "assistant", "content": "好的。"},
    {"role": "user", "content": "总共有几只宠物呢？"},
]

response = client.chat.completions.create(
    model="kimi-k2.5",
    messages=messages,
    stream=True,
)

for chunk in response:
    delta = chunk.choices[0].delta
    if hasattr(delta, "content") and delta.content:
        print(delta.content, end="", flush=True)

print()