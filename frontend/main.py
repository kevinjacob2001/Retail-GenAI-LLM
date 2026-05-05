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
from few_shots import few_shots


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
    example_selector = SemanticSimilarityExampleSelector(
        vectorstore=vector_store,
        k=2,
    )

    example_prompt = PromptTemplate(
        input_variables=["Question", "SQLQuery", "SQLResult","Answer",],
        template="\nQuestion: {Question}\nSQLQuery: {SQLQuery}\nSQLResult: {SQLResult}\nAnswer: {Answer}",
    )

    few_shot_prompt = FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=example_prompt,
        prefix=_mysql_prompt,
        suffix=PROMPT_SUFFIX,
        input_variables=["input", "table_info", "top_k"],
    )
    chain=SQLDatabaseChain.from_llm(
        llm,
        db,
        prompt=few_shot_prompt,
        verbose=True,
    )
    return chain

if __name__ == "__main__":
    chain = get_few_shot_Db_chain()
    print(chain.run("How many t-shirts do we have left for Nike in XS size and white color?"))