import sys
from pathlib import Path
import re

import streamlit as st
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX, _mysql_prompt
from langchain.prompts import FewShotPromptTemplate
from langchain.prompts.prompt import PromptTemplate
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from few_shots import few_shots
from gpt_client import llm


@st.cache_resource
def get_few_shot_db_chain() -> SQLDatabaseChain:
    db_user = "root"
    db_password = ""
    db_host = "localhost"
    db_port = 3306
    db_name = "atliq_tshirts"
    db = SQLDatabase.from_uri(
        f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}",
        sample_rows_in_table_info=5,
    )

    example_prompt = PromptTemplate(
        input_variables=["Question", "SQLQuery", "SQLResult", "Answer"],
        template=(
            "\nQuestion: {Question}\n"
            "SQLQuery: {SQLQuery}\n"
            "SQLResult: {SQLResult}\n"
            "Answer: {Answer}"
        ),
    )

    # Keep the few-shot behavior but avoid external embedding downloads.
    few_shot_prompt = FewShotPromptTemplate(
        examples=few_shots[:2],
        example_prompt=example_prompt,
        prefix=_mysql_prompt,
        suffix=PROMPT_SUFFIX,
        input_variables=["input", "table_info", "top_k"],
    )
    return SQLDatabaseChain.from_llm(
        llm,
        db,
        prompt=few_shot_prompt,
        verbose=False,
        return_direct=True,
    )


st.set_page_config(page_title="Retail SQL QA", page_icon="🛍️")
st.title("Retail SQL QA")
question = st.text_input("Ask a question")

if st.button("Submit", type="primary"):
    if not question.strip():
        st.warning("Please enter a question")
    else:
        try:
            chain = get_few_shot_db_chain()
            result = chain.invoke({"query": question})
            raw = str(result.get("result", result))
            match = re.search(r"Decimal\('([^']+)'\)|(-?\d+(?:\.\d+)?)", raw)
            final_answer = (match.group(1) or match.group(2)) if match else raw
            st.success(final_answer)
        except Exception as exc:  # noqa: BLE001
            st.error(f"Error: {exc}")