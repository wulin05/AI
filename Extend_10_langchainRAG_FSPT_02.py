"""
文件名FSPT: FewShotPromptTemplate: 提示词模板
组装FewShotPromptTemplate对象并获取最终提示词
"""
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_openai import ChatOpenAI
import os

example_template = PromptTemplate.from_template("单词: {word}, 反义词: {antonym}")

# 示例的动态数据注入: 格式必须是列表套字典: [{}]
example_data = [
    {"word": "大", "antonym": "小"},
    {"word": "上", "antonym": "下"}
]

few_shot_prompt = FewShotPromptTemplate(
    example_prompt = example_template,      # 示例数据的模板
    examples=example_data,                  # 示例的数据（用来注入动态示例数据）
    prefix="给出给定词的反义词,有如下示例:",
    suffix="基于示例告诉我: {input_word}的反义词是？",
    #声明在前缀或后缀中所需要注入的变量名,如上：input_word
    input_variables = ['input_word']
)

# #获得最终提示词,用下面的chain链就不能用字符串了，所以注释掉
# prompt_text = few_shot_prompt.invoke(input={"input_word": "左"}).to_string()
# print(prompt_text)

# 使用qwen3.5-plus,或kimi-k2.5模型，需要使用ChatOpenAI包！这边直接传入变量，让langchain自动处理
model = ChatOpenAI(
    model="kimi-k2.5",
    api_key=os.getenv("CODING_API_KEY"),
    base_url="https://coding.dashscope.aliyuncs.com/v1"
)

# 构建 chain 时用 prompt 对象，不是字符串
chain = few_shot_prompt | model

try:
    # 调用时动态传参
    response = chain.invoke({"input_word": "左"})
    
    # 安全检查
    if hasattr(response, 'content') and response.content:
        print(f"✅ AI 回答: {response.content}")
    else:
        print(f"⚠️ 响应异常: {response}")
        
except Exception as e:
    print(f"❌ 错误: {type(e).__name__} - {e}")