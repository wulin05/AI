md5_path = "./md5.text"

# Chroma 
collection_name = "rag"
persist_directory = "./chroma_db"


# 文本分割器
chunk_size = 1000         # 分割后的最大文本长度   
chunk_overlap = 100       # 连续文本段之间的字符重叠数量
separators = ["\n", "\n\n", ".", "。", "!", "?", ",", " ", ""]    # 自然段落的划分符号
max_split_char_number = 1000     # 文本分割的阈值,也就是当文本超过这个阈值才会被分割

# as_retriever检索器使用
similarity_threshold = 1  # 返回前3个最相关的结果

# 向量存储
embedding_model_name = "text-embedding-v4"
chat_model_name = "qwen-max"

# 将session_config放到这边
session_config = {
    "configurable": {
        "session_id": "linwu"
    }
}