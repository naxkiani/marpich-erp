FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

RUN pip install --no-cache-dir uvicorn[standard]

# Hatchling needs package trees before `pip install -e .` (pyproject alone is not enough).
COPY pyproject.toml ./
COPY shared ./shared
COPY core ./core
COPY contexts ./contexts
RUN pip install --no-cache-dir -e .

COPY . .

RUN adduser --disabled-password --gecos "" --uid 1000 app \
    && chown -R app:app /app

USER app

EXPOSE 8000
STOPSIGNAL SIGTERM
# Bind 0.0.0.0 for Compose/K8s. Do not treat 127.0.0.1 as a production hostname.
CMD ["uvicorn", "core.presentation.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
