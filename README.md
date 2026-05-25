# Status Factory

Mobile-first Goel Estates WhatsApp status generator built with FastAPI, Jinja2, Playwright, and Tailwind via CDN.

## What it does

- Accepts property details from a simple form.
- Generates two 1080x1920 status images.
- Uses a static navy/gold layout and a dynamic Unsplash-backed layout.
- Stores generated files locally and serves them back to the UI.
- Keeps a small generation history for quick regeneration.

## Local setup

1. Install Python 3.11+.
2. Install dependencies:

```bash
pip install -e .
playwright install chromium
```

3. Copy `.env.example` to `.env` and set `UNSPLASH_ACCESS_KEY` if you want live image lookup.
4. Run the app:

```bash
uvicorn app.main:app --reload
```

## Docker

```bash
docker build -t status-factory .
docker run -p 8000:8000 status-factory
```

## Notes

- Generated assets are written to `outputs/` and served from `/generated`.
- If Unsplash is unavailable, the app falls back to a branded SVG background.
- The screenshot pipeline uses Chromium through Playwright.
