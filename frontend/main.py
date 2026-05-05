import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from gpt_client import get_chat_llm, llm
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX, _mysql_prompt
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.prompts import FewShotPromptTemplate, SemanticSimilarityExampleSelector
from langchain.prompts.prompt import PromptTemplate
from langchain.vectorstores import Chroma
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain



llm = get_chat_llm(model="gpt-4o-mini", temperature=0, max_tokens=200)
llm.invoke("Hello, how are you?")


def get_few_shot_Db_chain():
    db_user="root"
    db_password=""
    db_host="localhost"
    db_port=3306
    db_name="atliq_tshirts"
    db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    ,sample_rows_in_table_info=5)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    to_vectorize=[" ".join(map(str, example.values())) for example in few_shots]
    vector_store = Chroma.from_texts(to_vectorize, embeddings,metadatas=few_shots)
    example_selector = SemanticSimilarityExampleSelector.from_examples(
        vectorstore=vector_store,
        k=2
    )


#use embeddings here

#use vector store here
vector_store = Chroma(embedding_function=embeddings, persist_directory="db_store")

#use example selector here