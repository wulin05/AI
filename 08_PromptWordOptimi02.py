from openai import OpenAI
import os
import json

api_key = os.getenv("CODING_API_KEY") or os.getenv("DASHSCOPE_API_KEY") or os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError(
        "Missing API key. Set CODING_API_KEY (preferred) or DASHSCOPE_API_KEY or OPENAI_API_KEY."
    )

client = OpenAI(
    api_key=api_key,
    base_url="https://coding.dashscope.aliyuncs.com/v1",
)

examples_data = {
    "是": [
        ("公司ABC发布了季度财报，显示盈利增长。", "财务披露，公司ABC利润上升。"),
        ("公司ITCAST发布了年度财报，显示盈利大幅度增长。", "财务披露，公司ITCAST更赚钱了。")
    ],
    "不是": [
        ("黄金价格下跌，投资者抛售。", "外汇市场交易额创下新高。"),
        ("央行降息，刺激经济增长。", "新能源技术创新。")
    ]
}

questions = [
    ("利率上升，影响房地产市场。", "高利率对房地产有一定的冲击。"),
    ("油价大幅度下跌，能源公司面临挑战。", "未来智能城市的建设趋势愈加明显。"),
    ("股票市场今日大跌，投资者信心受挫。", "持续下跌的市场让投资者感到担忧。")
]


messages = [
    {"role": "system", "content": f"你帮我完成文本匹配，我给你两个句子，被[]包围，你判断它们是否匹配，回答是或不是，请参考如下示例:"}
]

for key, value in examples_data.items():
    for v in value:
        messages.append({"role": "user", "content": f"文本1: [{v[0]}], 文本2: [{v[1]}]"})
        messages.append({"role": "assistant", "content": key})

for q in questions:
    request_message = {"role": "user", "content": f"文本1: [{q[0]}], 文本2: [{q[1]}]"}
    messages=messages + [request_message]
    print("\n=====本次请求的问题=====\n")
    print(messages[-1]["content"])

    response = client.chat.completions.create(
        model="kimi-k2.5",
        messages=messages,
        stream=True,
    )

    for chunk in response:
        delta = chunk.choices[0].delta
        if hasattr(delta, "content") and delta.content:
            print(delta.content, end="\n", flush=True)



