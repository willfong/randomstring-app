# Multi-stage Dockerfile for Python FastAPI application
# Base image: Python 3.12 Alpine for minimal size and security

# Stage 1: Builder - Install dependencies
FROM python:3.12-alpine AS builder

# Install uv for fast dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set working directory
WORKDIR /app

# Copy dependency files and README (required by pyproject.toml)
COPY pyproject.toml uv.lock README.md ./

# Install dependencies to a virtual environment
RUN uv sync --frozen --no-dev

# Stage 2: CSS Builder - Build Tailwind CSS
FROM node:22-alpine AS css-builder

# Set working directory
WORKDIR /app

# Copy package files
COPY package.json ./

# Install dependencies
RUN npm install

# Copy Tailwind config and source files
COPY tailwind.config.js ./
COPY src/static/css/input.css ./src/static/css/
COPY src/templates/ ./src/templates/

# Build CSS
RUN npm run build:css

# Stage 3: Runtime - Minimal production image
FROM python:3.12-alpine AS runtime

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH" \
    PORT=8000

# Install runtime dependencies only
RUN apk add --no-cache \
    tini \
    && rm -rf /var/cache/apk/*

# Create non-root user for security
RUN addgroup -g 1001 -S appuser && \
    adduser -S -D -H -u 1001 -h /app -s /sbin/nologin -G appuser -g appuser appuser

# Set working directory
WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder --chown=appuser:appuser /app/.venv /app/.venv

# Copy compiled CSS from css-builder
COPY --from=css-builder --chown=appuser:appuser /app/src/static/css/output.css /app/src/static/css/output.css

# Copy application code
COPY --chown=appuser:appuser src/ /app/src/
COPY --chown=appuser:appuser pyproject.toml /app/

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:${PORT}/health').read()" || exit 1

# Expose port
EXPOSE 8000

# Use tini as init system for proper signal handling
ENTRYPOINT ["/sbin/tini", "--"]

# Run the application with uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--no-access-log"]
