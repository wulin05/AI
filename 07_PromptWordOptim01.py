import json
from openai import OpenAI
import os

api_key = os.getenv("CODING_API_KEY") or os.getenv("DASHSCOPE_API_KEY") or os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError(
        "Missing API key. Set CODING_API_KEY (preferred) or DASHSCOPE_API_KEY or OPENAI_API_KEY."
        )           

client = OpenAI(
    api_key=api_key,
    base_url="https://coding.dashscope.aliyuncs.com/v1",
)

schema = ["日期", "股票名称", "开盘价", "收盘价", "成交量"]

examples_data= [
    {
        "content": "2023-01-10,股市震荡,股票强大科技A股今日开盘价100人民币,一度飙升至105人民币,随后回落至98人民币,最终收盘价为102人民币,成交量为52万股",
        "answer": {
            "日期": "2023-01-10",
            "股票名称": "强大科技A股",
            "开盘价": "100人民币",
            "收盘价": "102人民币",
            "成交量": "520000"
        }
    },
    {
        "content": "2024-05-16,股市利好。股票英伟达美股今日开盘价105美元，一股飙升至109没有，随后回落至100美元，最终以116美元收盘，成交量达到356万股。",
        "answer": {
            "日期": "2024-05-16",
            "股票名称": "英伟达美股",
            "开盘价": "105美元",
            "收盘价": "116美元",
            "成交量": "3560000"
        }
    },
]

questions = [
    "2025-06-16,股市利好。股票苹果美股今日开盘价150美元，一度飙升至155美元，随后回落至148美元，最终以152美元收盘，成交量达到500万股。",
    "2024-06-02,股市利空。股票微软美股今日开盘价200美元，一度飙升至210美元，随后回落至195美元，最终以198美元收盘，成交量达到400万股。",
    "2024-06-10,股市震荡。股票alibaba今日开盘价30人民币，一度飙升至320人民币，随后回落至290人民币，最终以310人民币收盘。",
]

messages = [
    {"role": "system", "content": f"你是金融专家，按照以下示例提取{schema}文本中的关键信息，按JSON字符串输出，如果某些信息不存在，用'原文未提及'表示，请参考如下示例："},
]

for value in examples_data:
    messages.append({"role": "user", "content": value["content"]})
    messages.append({"role": "assistant", "content": json.dumps(value["answer"], ensure_ascii=False)})
    # messages.append({"role": "assistant", "content": value["answer"]}) # 直接传字典，qwen3.5-plus模型会报错..

for x in messages:
    print(f"{x['role']}:{x['content']}\n")

for q in questions:
    response = client.chat.completions.create(
        model="kimi-k2.5",
        messages=messages+[{"role":"user", "content":f"按照示例，提取这段文本的关键信息: {q}"}],
        stream=True # 如果是False则一次性返回完整内容（默认），True则流式返回增量内容
    )
    # 不能直接打印，需要累加流式数据
    # print(response.choices[0].message.content)  

    full_content = ""
    for chunk in response:
        if chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            full_content += content
            print(content, end="", flush=True)
    print()
