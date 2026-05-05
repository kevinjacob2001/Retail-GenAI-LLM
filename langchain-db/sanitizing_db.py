"""SQLDatabase that strips markdown code fences from LLM output before execution."""

from __future__ import annotations

import re

from langchain_community.utilities.sql_database import SQLDatabase

_FENCED = re.compile(r"```(?:sql)?\s*(.*?)```", re.DOTALL | re.IGNORECASE)


def sanitize_generated_sql(sql: str) -> str:
    s = sql.strip()
    if "SQLQuery:" in s:
        s = s.split("SQLQuery:", 1)[-1].strip()
    m = _FENCED.search(s)
    if m:
        return m.group(1).strip()
    if s.startswith("```"):
        s = re.sub(r"^```(?:sql)?\s*", "", s, flags=re.IGNORECASE).strip()
        if s.endswith("```"):
            s = s[:-3].strip()
    return s


class SanitizingSQLDatabase(SQLDatabase):
    def run(self, command, *args, **kwargs):  # type: ignore[no-untyped-def]
        return super().run(sanitize_generated_sql(str(command)), *args, **kwargs)
