from email import message
from multiprocessing import Value
from pydoc import cli
from pyexpat.errors import messages
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

examples_data= {
    "新闻报道": '今日，股市经理了一轮震荡，收到宏观经济数据和全球贸易紧张局势的影响，投资者密切关注美联储可能的政策调整，以适应市场的不确定性。',
    "财务报告":'本公司年度财务报告显示，去年公司实现了稳步增长的盈利，同时资产负债表呈现强劲的状况。经济环境的文档和管理层的有效战略执行为公司的健康发展....',
    "公司公告":'本公司高兴地宣布成功完成最新一轮并购交易，收购了一家在人工智能领域领先的公司。这一战略举措有助于扩大我们的业务领域，提高市场竞争力',
    "分析师报告": '最新的行业分析报告指出，科技公司的创新将成为未来增长的主要推动力。云计算,人工智能和数字化转型被认为是引领行业发展的关键因素。',
}

examples_types = ['新闻报道', '财务报告', '公司公告', '分析师报告']

questions = [
    "今日，央行发布公告宣布降低利率，以刺激经济增长。这一降息举措将影响贷款利率，并在未来几个季度内对金融市场产生影响。",
    "ABC公司今日发布公告成,已成功完成对XYZ公司股权的收购交易。本次交易是ABC公司在扩大业务范围,加强市场竞争力方面的重要举措。据悉,此次收购将进一步巩固....",
    "公司资产负债表显示，公司偿债能力强劲，现金流充足，为未来投资和扩张提供了坚实的财务基础。",
    "最新的分析报告指出，可再生能源行业预计在未来几年经历持续增长，投资者应该关注这一领域的投资机会",
    "小强喜欢小艾哟"
]

messages = [
    {"role": "system", "content": "你是金融专家，将文本分类为['新闻报道', '财务报告'，'公司公告'，'分析师报告']，不清楚的分类为'不清楚类别',下面有示例:"},
]

for key,value in examples_data.items():
    messages.append({"role": "user", "content": value})
    messages.append({"role": "assistant", "content": key})

# 向模型提问
for q in questions:
    response = client.chat.completions.create(
        # model="qwen3.5-plus",
        model="kimi-k2.5",
        # model="glm-5",
        messages=messages+[{"role":"user", "content":f"按照示例，回答这段文本的分类类别: {q}"}]
    )
    print(response.choices[0].message.content)


# messages = [
#     {"role": "system", "content": "你是金融专家，将文本分类为['新闻报道', '财务报告'，'公司公告'，'分析师报告']，不清楚的分类为'不清楚类别',下面有示例:"},
    
#     {"role": "user", "content": "今日，央行发布最新货币政策，决定将基准利率下调0.25个百分点。"},
#     {"role": "assistant", "content": "新闻报道"},
#     {"role": "user", "content": "ABC公司发布最新财报，营收1000亿元，净利润100亿元。"},
#     {"role": "assistant", "content": "财务报告"},
#     {"role": "user", "content": "公司资产负债表显示，公司偿债能力较强，现金流充足......"},
#     {"role": "assistant", "content": "公司公告"},
#     {"role": "user", "content":"最新的分析报告指出, 可再生能源..........."},
#     {"role": "assistant", "content":"分析师报告"}，
# ]
