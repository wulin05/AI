"""
文件名FSPT: FewShotPromptTemplate: 提示词模板
组装FewShotPromptTemplate对象并获取最终提示词
"""
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_community.llms.tongyi import Tongyi

example_template = PromptTemplate.from_template("单词: {word}, 反义词: {antonym}, 英文: {english}")

# 示例的动态数据注入: 格式必须是列表套字典: [{}]
example_data = [
    {"word": "大", "antonym": "小", "english": "big"},
    {"word": "上", "antonym": "下", "english": "up"}
]

few_shot_prompt = FewShotPromptTemplate(
    example_prompt = example_template,      # 示例数据的模板
    examples=example_data,                  # 示例的数据（用来注入动态示例数据）
    prefix="请给出给定的词的反义词,英文,如下示例:",
    suffix="基于示例告诉我: {input_word}的反义词和英文分别是?",
    #声明在前缀或后缀中所需要注入的变量名,如上：input_word
    input_variables = ['input_word']
)

"""

#获得最终提示词
prompt_text = few_shot_prompt.invoke(input={"input_word": "左"}).to_string()
# print(prompt_text)

model = Tongyi(model="qwen-max")
res = model.invoke(input=prompt_text)
print(res)

"""


# 如果是多个输入word：
# 调用时传入用分隔符连接的字符串
words_list = ["左", "右", "高", "低", "大", "小", "上", "下", "前", "后"]
prompt_text = few_shot_prompt.invoke(input={"input_word": "、".join(words_list)}).to_string()
print(prompt_text)

model = Tongyi(model="qwen-max")
# model = Tongyi(model="qwen3.5-plus")

# 流式输出
res = ""
for chunk in model.stream(input=prompt_text):
    print(chunk, end="", flush=True)
    res += chunk

print() 
