""" 
from langchain_ollama import OllamaLLM

llm = OllamaLLM(model='qwen2.5:1.5b', temperature=0.7)
res = llm.invoke("帮我讲个笑话吧")
print(res) 

"""

""" 
from langchain_ollama import ChatOllama

chat = ChatOllama(model='qwen2.5:1.5b', temperature=0.7)
res = chat.invoke("帮我讲个笑话吧")
print(res.content) 

"""

""" 
from langchain_ollama import OllamaLLM
llm = OllamaLLM(model='llama3.2:3b', temperature=0.7)
res = llm.invoke("帮我讲个笑话吧")
if hasattr(res, "content") and res.content:
    print(res.content)
else:
    print(res) 

"""

from langchain_ollama import ChatOllama

chat = ChatOllama(model='deepseek-coder:1.3b', temperature=0.7)
res = chat.stream("你是谁呀能做什么？")
for chunk in res:
    if hasattr(chunk, "content") and chunk.content:
        print(chunk.content, end="", flush=True)