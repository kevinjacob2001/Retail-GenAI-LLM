# Retail GenAI LLM

A basic project for querying a retail t-shirt inventory database using LangChain, OpenAI, and MySQL.

## Features

- Natural language to SQL query flow
- Few-shot prompting support
- Streamlit frontend for asking questions

## Project Structure

- `frontend/` - Streamlit app and helper modules
- `langchain-db/` - Notebook experiments and SQL chain setup
- `gpt_client.py` - Shared OpenAI/LangChain client setup
- `database/` - SQL schema script

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:
   - `pip install -r requirements.txt`
3. Add your API key in `.env`:
   - `OPENAI_API_KEY=...`

## Run

- Start frontend app:
  - `streamlit run frontend/main.py`