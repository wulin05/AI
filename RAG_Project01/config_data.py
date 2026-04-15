md5_path = "./RAG_Project01/md5.text"

# Chroma 
collection_name = "rag"
persist_directory = "./RAG_Project01/chroma_db"


# 文本分割器
chunk_size = 1000
chunk_overlap = 100
separators = ["\n", "\n\n", ".", "。", "!", "?", ",", " ", ""]
max_split_char_number = 1000    # 降低阈值，让短文本也能被处理

# as_retriever检索器使用
similarity_threshold = 1  # 返回前3个最相关的结果

# 向量存储
embedding_model_name = "text-embedding-v4"
chat_model_name = "qwen3-max"