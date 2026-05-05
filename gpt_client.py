import os
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent

try:
    from langchain_openai import ChatOpenAI
except ModuleNotFoundError:
    venv_py = _ROOT / ".venv" / "bin" / "python"
    win_py = _ROOT / ".venv" / "Scripts" / "python.exe"
    target = venv_py if venv_py.is_file() else win_py if win_py.is_file() else None
    if target and os.path.realpath(sys.executable) != os.path.realpath(target):
        os.execv(str(target), [str(target), __file__, *sys.argv[1:]])
    raise SystemExit(
        "Missing package 'langchain-openai'. From the project root run:\n"
        "  python3 -m venv .venv && .venv/bin/pip install -r requirements.txt\n"
        "Then: .venv/bin/python gpt_client.py"
    ) from None

from dotenv import load_dotenv
from pydantic import SecretStr

load_dotenv(_ROOT / ".env")


def get_chat_llm(
    *,
    model: str = "gpt-4o-mini",
    temperature: float = 0.7,
    max_tokens: int = 150,
) -> ChatOpenAI:
    """LangChain chat model — pass this as `llm` into chains and agents."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Set OPENAI_API_KEY in the environment or in a .env file.")
    return ChatOpenAI(
        model=model,
        temperature=temperature,
        max_completion_tokens=max_tokens,
        api_key=SecretStr(api_key),
    )


def generate_chatgpt_response(prompt: str, *, model: str = "gpt-4o-mini") -> str:
    llm_obj = get_chat_llm(model=model)
    msg = llm_obj.invoke(prompt)
    content = msg.content
    if content is None:
        return ""
    if isinstance(content, str):
        return content.strip()
    return str(content).strip()


llm = get_chat_llm(temperature=0, max_tokens=512)


if __name__ == "__main__":
    text = input("Ask ChatGPT: ")
    print(generate_chatgpt_response(text))
