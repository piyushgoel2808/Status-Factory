from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import requests

from app.core.config import settings, svg_fallback_data_uri
from app.models.schemas import BackgroundAsset


@dataclass(frozen=True)
class UnsplashResult:
    asset: BackgroundAsset
    error: str | None = None


def _build_fallback(query: str, reason: str | None = None) -> BackgroundAsset:
    return BackgroundAsset(
        source="fallback",
        query=query,
        url=svg_fallback_data_uri(),
        photographer="Status Factory",
        credit_url=None,
    )


def fetch_background_asset(queries: Iterable[str] | None = None) -> BackgroundAsset:
    available_queries = tuple(queries or settings.unsplash_queries)
    if not settings.unsplash_access_key:
        return _build_fallback(available_queries[0], "missing_api_key")

    last_error: str | None = None
    for query in available_queries:
        try:
            response = requests.get(
                "https://api.unsplash.com/photos/random",
                params={
                    "query": query,
                    "orientation": "portrait",
                    "content_filter": "high",
                    "count": 1,
                },
                headers={"Authorization": f"Client-ID {settings.unsplash_access_key}"},
                timeout=15,
            )
            response.raise_for_status()
            payload = response.json()
            if isinstance(payload, list):
                payload = payload[0]
            urls = payload.get("urls", {})
            user = payload.get("user", {})
            links = payload.get("links", {})
            image_url = urls.get("full") or urls.get("regular") or urls.get("raw")
            if not image_url:
                raise ValueError("Unsplash response missing image URL")
            return BackgroundAsset(
                source="unsplash",
                query=query,
                url=image_url,
                photographer=user.get("name"),
                credit_url=links.get("html"),
            )
        except Exception as exc:  # pragma: no cover - network fallback
            last_error = str(exc)

    return _build_fallback(available_queries[0], last_error)
