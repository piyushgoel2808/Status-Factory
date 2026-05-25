from __future__ import annotations

import json
import re
from datetime import datetime, timezone

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.core.config import file_to_data_uri, settings
from app.models.schemas import GeneratedImage, GenerationResponse, StatusRequest
from app.services.render import RenderService, file_to_base64
from app.services.storage import GenerationStore, now_utc
from app.services.unsplash import fetch_background_asset


app = FastAPI(title=settings.app_name)
templates = Jinja2Templates(directory=str(settings.templates_dir))
store = GenerationStore(settings.history_path)
renderer = RenderService()

app.mount("/generated", StaticFiles(directory=str(settings.outputs_dir)), name="generated")


def parse_features(value: str) -> list[str]:
    items = [item.strip() for item in value.split(",")]
    return [item for item in items if item]


def slugify(value: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return normalized or "status"


def build_caption(request_data: StatusRequest, features: list[str]) -> str:
    feature_text = " | ".join(features[:4]) if features else "Ready for viewing"
    return (
        f"Goel Estates | {request_data.property_type} | {request_data.location} | {request_data.price} | "
        f"{feature_text} | CONTACT NAVNEET GOEL | 7042636062 | 9999731256 | BANK FINANCE FACILITY AVAILABLE"
    )


def generate_images(request_data: StatusRequest) -> GenerationResponse:
    settings.ensure_runtime_dirs()
    features = parse_features(request_data.key_features)
    background = fetch_background_asset()
    generated_id = store.create_id()
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    base_name = f"{timestamp}-{slugify(request_data.property_type)}-{generated_id[:8]}"

    shared_context: dict[str, object] = {
        "property_type": request_data.property_type,
        "location": request_data.location,
        "price": request_data.price,
        "features": features,
        "features_summary": " | ".join(features) if features else "Available on request",
        "contact_line": "CONTACT NAVNEET GOEL | 7042636062 | 9999731256 | BANK FINANCE FACILITY AVAILABLE",
        "logo_data_uri": file_to_data_uri(settings.logo_path),
        "layout_variant": request_data.layout_variant,
        "brand_gold": "#c8a24a",
        "brand_navy": "#071a33",
        "rendered_at": now_utc().isoformat(),
    }

    static_html = renderer.render_template(
        "status_static.html",
        {
            **shared_context,
            "template_name": "static",
            "background_url": None,
        },
    )
    static_path = settings.outputs_dir / f"{base_name}-static.jpg"
    renderer.capture_jpeg(static_html, static_path)

    dynamic_html = renderer.render_template(
        "status_dynamic.html",
        {
            **shared_context,
            "template_name": "dynamic",
            "background_url": background.url,
            "background_source": background.source,
            "background_query": background.query,
        },
    )
    dynamic_path = settings.outputs_dir / f"{base_name}-dynamic.jpg"
    renderer.capture_jpeg(dynamic_html, dynamic_path)

    caption = build_caption(request_data, features)
    response = GenerationResponse(
        id=generated_id,
        created_at=now_utc(),
        request=request_data,
        caption=caption,
        background=background,
        images=[
            GeneratedImage(
                kind="static",
                filename=static_path.name,
                url=f"/generated/{static_path.name}",
                base64=file_to_base64(static_path),
            ),
            GeneratedImage(
                kind="dynamic",
                filename=dynamic_path.name,
                url=f"/generated/{dynamic_path.name}",
                base64=file_to_base64(dynamic_path),
            ),
        ],
    )
    store.add(response)
    return response


@app.get("/")
def home(request: Request):
    recent = store.list_recent(12)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "app_name": settings.app_name,
            "recent_generations": recent,
            "recent_generations_json": json.dumps([item.model_dump(mode="json") for item in recent]),
            "logo_data_uri": file_to_data_uri(settings.logo_path),
            "business_card_data_uri": file_to_data_uri(settings.business_card_path),
            "whatsapp_reference_data_uri": file_to_data_uri(settings.whatsapp_reference_path),
            "whatsapp_reference_alt_data_uri": file_to_data_uri(settings.whatsapp_reference_alt_path),
            "default_request": {
                "property_type": "Builder Floor",
                "location": "South Delhi",
                "price": "₹2.85 Cr",
                "key_features": "Park facing, modular kitchen, lift, stilt parking",
            },
        },
    )


@app.get("/api/history")
def history():
    return {"records": [item.model_dump(mode="json") for item in store.list_recent(24)]}


@app.post("/generate-status")
def generate_status(
    property_type: str = Form(...),
    location: str = Form(...),
    price: str = Form(...),
    key_features: str = Form(""),
    layout_variant: str = Form("balanced"),
):
    try:
        request_data = StatusRequest.model_validate(
            {
                "property_type": property_type,
                "location": location.strip(),
                "price": price.strip(),
                "key_features": key_features.strip(),
                "layout_variant": layout_variant.strip() or "balanced",
            }
        )
    except Exception as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    try:
        response = generate_images(request_data)
        return JSONResponse(response.model_dump(mode="json"))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Generation failed: {exc}") from exc


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.get("/favicon.ico")
def favicon_redirect():
    return Response(status_code=204)
