# 注意噢，这个是serve.py 文件的所有内容。 千万别在Jupyter Notebook 运行！
#!/usr/bin/env python
from typing import List

from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_zhipu import ChatZhipuAI
from langserve import add_routes
import getpass
import os

os.environ["ZHIPUAI_API_KEY"] = getpass.getpass()

# 1. Create prompt template
system_template = "将以下内容翻译成 {language}:"
prompt_template = ChatPromptTemplate.from_messages([
    ('system', system_template),
    ('user', '{text}')
])

# 2. Create model
model = ChatZhipuAI(model="glm-3-turbo")


# 3. Create parser
parser = StrOutputParser()

# 4. Create chain
chain = prompt_template | model | parser


# 4. App definition
app = FastAPI(
  title="LangChain Server",
  version="1.0",
  description="A simple API server using LangChain's Runnable interfaces",
)

# 5. Adding chain route

add_routes(
    app,
    chain,
    path="/chain",
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)