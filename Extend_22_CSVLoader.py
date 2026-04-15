from langchain_community.document_loaders.csv_loader import CSVLoader

# loader = CSVLoader(
#     file_path="./data/people.csv",
#     encoding="utf-8"
# )
loader = CSVLoader(
    file_path="./data/people.csv",
    csv_args={
        "delimiter": "," ,     # 指定分隔符
        # "delimiter": "|",    # 指定分隔符
        # "quotechar": '"',      # 表示""里面的分隔符不作为分隔符
        # "fieldnames": ['a', 'b', 'c', 'd']  # 这个是说用这些字符当表头
    },
    encoding="utf-8"
)

# # 批量加载.load() -> [Document, Document...]
# documents = loader.load()

# # print(documents)
# for doc in documents:
#     print(type(doc), doc)


# 懒加载 .lazy_load() 迭代器[Document]
for doc in loader.lazy_load():
    print(doc)