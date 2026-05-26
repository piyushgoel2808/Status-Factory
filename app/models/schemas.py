from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class StatusRequest(BaseModel):
    property_type: str = Field(min_length=2, max_length=100)
    location: str = Field(min_length=2, max_length=120)
    price: str = Field(min_length=1, max_length=80)
    key_features: str = Field(default="", max_length=400)
    layout_variant: Literal["balanced", "asymmetric"] = "balanced"
    scale_global: float = 1.0
    scale_logo: float = 1.65
    scale_brand: float = 1.0
    scale_header: float = 1.0
    scale_text: float = 1.0
    scale_footer: float = 1.0
    canvas_format: Literal["whatsapp", "instagram_square", "instagram_portrait", "custom"] = "whatsapp"
    custom_width: int | None = None
    custom_height: int | None = None


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
