import os
import sys
from pathlib import Path
from langchain_community.llms import OpenAI
_ROOT = Path(__file__).resolve().parents[1]

try:
    from openai import OpenAI
except ModuleNotFoundError:
    venv_py = _ROOT / ".venv" / "bin" / "python"
    win_py = _ROOT / ".venv" / "Scripts" / "python.exe"
    target = venv_py if venv_py.is_file() else win_py if win_py.is_file() else None
    if target and os.path.realpath(sys.executable) != os.path.realpath(target):
        os.execv(str(target), [str(target), __file__, *sys.argv[1:]])
    raise SystemExit(
        "Missing package 'openai'. From the project root run:\n"
        "  python3 -m venv .venv && .venv/bin/pip install -r requirements.txt\n"
        "Then: chatgpt-client/../.venv/bin/python chatgpt-client/gpt-client.py"
    ) from None

from dotenv import load_dotenv

load_dotenv(_ROOT / ".env")


def generate_chatgpt_response(prompt: str, *, model: str = "gpt-4o-mini") -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Set OPENAI_API_KEY in the environment or in a .env file.")

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
        temperature=0.7,
    )
    content = response.choices[0].message.content
    return content.strip() if content else ""


if __name__ == "__main__":
    text = input("Ask ChatGPT: ")
    print(generate_chatgpt_response(text))
