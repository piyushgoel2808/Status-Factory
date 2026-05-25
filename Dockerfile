FROM python:3.11-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PLAYWRIGHT_BROWSERS_PATH=0

WORKDIR /app

COPY pyproject.toml README.md ./
COPY app ./app
COPY templates ./templates
COPY logo.jpeg ./
COPY "bussiness card.jpeg" ./
COPY "WhatsApp Image 2026-05-25 at 10.33.25 PM.jpeg" ./
COPY "WhatsApp Image 2026-05-25 at 10.33.25 PM (1).jpeg" ./

RUN pip install --no-cache-dir . && python -m playwright install --with-deps chromium

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
