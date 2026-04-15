# Langchain 安装指南

## 第三方依赖，建议不要全局安装

```bash
source ~/.venv/bin/activate
pip install langchain langchain-community langchain-ollama dashscope chromadb

```

## 测试是否导包成功

```bash
python
import langchain
```

## 各包说明

- langchain: 核心包
- langchain-community: 社区支持包，提供了更多的第三方模型调用（比如阿里云千问模型就需要这个包）
- langchain-ollama: Ollama支持包，支持调用Ollama托管部署的本地模型
- dashscope：阿里云通义千问的Python SDK
- chromadb: 轻量向量数据库

## 建议保存依赖

比如放在项目目录下

```bash
pip freeze > ./requirements.txt
cd ../new_project
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

```

![alt text](image.png)
