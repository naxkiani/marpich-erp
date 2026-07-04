FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir uvicorn[standard]

COPY pyproject.toml .
RUN pip install --no-cache-dir -e .

COPY . .

EXPOSE 8000
CMD ["uvicorn", "core.presentation.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
