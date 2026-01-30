FROM python:3.13-slim

ARG APP_HOME=/rbac-chatbot
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=$APP_HOME

WORKDIR $APP_HOME

# Copy requirements first for cache-friendly builds
COPY requirements.txt .

# Install build deps, install Python deps, then remove build deps in the same RUN
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get purge -y --auto-remove build-essential && \
    rm -rf /var/lib/apt/lists/*

# Create app user / group
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# Copy application files
COPY app/ $APP_HOME/app/
COPY ui/ $APP_HOME/ui/
COPY resources/ $APP_HOME/resources/


# Fix ownership (use APP_HOME, not /app)
RUN chown -R appuser:appgroup $APP_HOME

# Switch to non-root user
USER appuser

# streamlit port
#EXPOSE 8002

# fastapi port
#EXPOSE 8000

# Healthcheck using Python stdlib (no extra deps required)
# HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
#   CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/health',timeout=10).getcode()==200 else 1)"

# Run the app
CMD ["python", "app/main.py"]