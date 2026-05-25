# 1. Use the official Microsoft Playwright image (Browser is already installed!)
FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

# 2. Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# 3. Copy your project configuration files first
COPY pyproject.toml README.md ./

# 4. Install your Python packages (no need to install Playwright browsers here)
RUN pip install --no-cache-dir .

# 5. Copy your application code
COPY app ./app
COPY templates ./templates

# 6. Copy your brand assets
COPY logo.jpeg ./
COPY "bussiness card.jpeg" ./
COPY "WhatsApp Image 2026-05-25 at 10.33.25 PM.jpeg" ./
COPY "WhatsApp Image 2026-05-25 at 10.33.25 PM (1).jpeg" ./

# 7. Expose the port
EXPOSE 8000

# 8. Start the server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]