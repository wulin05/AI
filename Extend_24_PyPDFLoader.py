"""
LangChain内支持许多PDF的加载器,选择其中的PyPDFLoader使用
PyPDFLoader加载器依赖PyPDF2库,需要额外安装: 
pip install pypdf

"""
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader(
    file_path="./data/cka.pdf",
    # mode="page",   # 默认就是page模式,即每一页作为一个Document对象
    mode="single", # single模式,即不管PDF有多少页,整个PDF作为一个Document对象
    # password="123456"   # 如果PDF有密码,可以在这里指定,如果没有密码,则不需要这个参数
)

i=0
# for doc in loader.load():
#     i+=1
#     print(f"第{i}页的内容是:\n{doc.page_content}\n\n")

for doc in loader.lazy_load():
    i+=1
    print(f"第{i}页的内容是:\n{doc.page_content}\n\n")