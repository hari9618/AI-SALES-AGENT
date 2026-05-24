# ──────────────────────────────────────────────────────────────
# Stage 1: Builder — install dependencies
# ──────────────────────────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /build

# Install build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc libffi-dev libssl-dev curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies into a target directory
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir --prefix=/install -r requirements.txt


# ──────────────────────────────────────────────────────────────
# Stage 2: Runtime image
# ──────────────────────────────────────────────────────────────
FROM python:3.11-slim AS runtime

LABEL maintainer="your-email@company.com"
LABEL version="1.0.0"
LABEL description="AI Sales Automation & Lead Intelligence System"

# Copy installed packages from builder
COPY --from=builder /install /usr/local

WORKDIR /app

# Copy application code
COPY app/          ./app/
COPY streamlit_app/ ./streamlit_app/
COPY workflows/    ./workflows/
COPY .env.example  ./.env.example

# Create non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser /app
USER appuser

# Expose ports
EXPOSE 8000   
EXPOSE 8501   

# Default: run FastAPI (overridden in docker-compose for Streamlit)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
