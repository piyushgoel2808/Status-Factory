from __future__ import annotations

import base64
import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "Status Factory")
    host: str = os.getenv("APP_HOST", "0.0.0.0")
    port: int = int(os.getenv("APP_PORT", "8000"))
    debug: bool = os.getenv("APP_DEBUG", "false").lower() in {"1", "true", "yes", "on"}
    unsplash_access_key: str | None = os.getenv("UNSPLASH_ACCESS_KEY") or None
    outputs_dir: Path = BASE_DIR / "outputs"
    templates_dir: Path = BASE_DIR / "templates"
    logo_path: Path = BASE_DIR / "logo1.png"
    business_card_path: Path = BASE_DIR / "bussiness card.jpeg"
    whatsapp_reference_path: Path = BASE_DIR / "WhatsApp Image 2026-05-25 at 10.33.25 PM.jpeg"
    whatsapp_reference_alt_path: Path = BASE_DIR / "WhatsApp Image 2026-05-25 at 10.33.25 PM (1).jpeg"
    history_path: Path = outputs_dir / "history.json"
    max_history_items: int = 24
    unsplash_queries: tuple[str, str] = ("luxury living room", "modern apartment building")

    def ensure_runtime_dirs(self) -> None:
        self.outputs_dir.mkdir(parents=True, exist_ok=True)


settings = Settings()
settings.ensure_runtime_dirs()


def file_to_data_uri(path: Path, mime_type: str = "image/jpeg") -> str:
    if not path.exists():
        return ""
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def svg_fallback_data_uri(title: str = "Goel Estates") -> str:
    svg = f"""
    <svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920" viewBox="0 0 1080 1920">
      <defs>
        <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stop-color="#071a33"/>
          <stop offset="100%" stop-color="#02070f"/>
        </linearGradient>
        <radialGradient id="r" cx="35%" cy="22%" r="80%">
          <stop offset="0%" stop-color="#caa34d" stop-opacity="0.35"/>
          <stop offset="100%" stop-color="#caa34d" stop-opacity="0"/>
        </radialGradient>
        <radialGradient id="r2" cx="70%" cy="78%" r="55%">
          <stop offset="0%" stop-color="#11315d" stop-opacity="0.55"/>
          <stop offset="100%" stop-color="#11315d" stop-opacity="0"/>
        </radialGradient>
      </defs>
      <rect width="1080" height="1920" fill="url(#g)"/>
      <circle cx="280" cy="350" r="430" fill="url(#r)"/>
      <circle cx="860" cy="1650" r="360" fill="url(#r2)"/>
      <path d="M-80 1540C180 1380 340 1500 560 1410C800 1310 900 1130 1160 1220V1960H-80Z" fill="#081f3d" fill-opacity="0.72"/>
      <path d="M0 260C190 180 340 220 520 190C700 160 840 56 1080 100V0H0Z" fill="#0f2b53" fill-opacity="0.52"/>
      <rect x="88" y="165" width="220" height="4" rx="2" fill="#caa34d" fill-opacity="0.45"/>
      <rect x="772" y="1675" width="220" height="4" rx="2" fill="#caa34d" fill-opacity="0.28"/>
    </svg>
    """.strip()
    encoded = base64.b64encode(svg.encode("utf-8")).decode("ascii")
    return f"data:image/svg+xml;base64,{encoded}"
