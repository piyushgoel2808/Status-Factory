from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class StatusRequest(BaseModel):
    property_type: Literal["Kothi", "Builder Floor", "DDA Flat"]
    location: str = Field(min_length=2, max_length=120)
    price: str = Field(min_length=1, max_length=80)
    key_features: str = Field(default="", max_length=400)
    layout_variant: Literal["balanced", "asymmetric"] = "balanced"


class GeneratedImage(BaseModel):
    kind: Literal["static", "dynamic"]
    filename: str
    url: str
    base64: str


class BackgroundAsset(BaseModel):
    source: str
    query: str | None = None
    url: str
    photographer: str | None = None
    credit_url: str | None = None


class HistoryItem(BaseModel):
    id: str
    created_at: datetime
    request: StatusRequest
    caption: str
    background: BackgroundAsset
    images: list[GeneratedImage]


class GenerationResponse(BaseModel):
    id: str
    created_at: datetime
    request: StatusRequest
    caption: str
    background: BackgroundAsset
    images: list[GeneratedImage]
