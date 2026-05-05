"""Notebook-friendly import for the shared ChatOpenAI factory (hyphenated chatgpt-client path)."""

import importlib.util
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location(
    "_chatgpt_client_impl",
    _ROOT / "chatgpt-client" / "gpt-client.py",
)
if _spec is None:
    raise ImportError("spec_from_file_location returned None")
_loader = _spec.loader
if _loader is None:
    raise ImportError("module spec has no loader")
_mod = importlib.util.module_from_spec(_spec)
_loader.exec_module(_mod)

get_chat_llm = _mod.get_chat_llm
generate_chatgpt_response = _mod.generate_chatgpt_response
llm = get_chat_llm(temperature=0, max_tokens=512)
