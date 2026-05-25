from __future__ import annotations

import base64
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape
from playwright.sync_api import sync_playwright

from app.core.config import settings


class RenderService:
    def __init__(self) -> None:
        self.environment = Environment(
            loader=FileSystemLoader(str(settings.templates_dir)),
            autoescape=select_autoescape(["html", "xml"]),
        )

    def render_template(self, template_name: str, context: dict[str, Any]) -> str:
        template = self.environment.get_template(template_name)
        return template.render(**context)

    def capture_jpeg(self, html: str, output_path: Path) -> None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True, args=["--disable-dev-shm-usage"])
            try:
                page = browser.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
                page.set_content(html, wait_until="networkidle")
                page.screenshot(path=str(output_path), type="jpeg", quality=94, full_page=False)
            finally:
                browser.close()


def file_to_base64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("ascii")
