from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from app.core.config import settings
from app.models.schemas import GenerationResponse, HistoryItem


class GenerationStore:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _read(self) -> list[dict]:
        if not self.path.exists():
            return []
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                return list(data.get("records", []))
            if isinstance(data, list):
                return data
        except json.JSONDecodeError:
            return []
        return []

    def _write(self, records: list[dict]) -> None:
        payload = {"records": records[: settings.max_history_items]}
        self.path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, default=str), encoding="utf-8")

    def add(self, response: GenerationResponse) -> HistoryItem:
        records = self._read()
        item = HistoryItem.model_validate(response.model_dump())
        records.insert(0, item.model_dump(mode="json"))
        self._write(records)
        return item

    def list_recent(self, limit: int | None = None) -> list[HistoryItem]:
        records = self._read()
        limited = records[: limit or settings.max_history_items]
        return [HistoryItem.model_validate(record) for record in limited]

    def create_id(self) -> str:
        return uuid4().hex


def now_utc() -> datetime:
    return datetime.now(timezone.utc)
