FROM python:3.14 AS builder

WORKDIR /app

RUN pip install --no-cache-dir pipenv==2025.0.3

COPY Pipfile Pipfile.lock ./

RUN PIPENV_VENV_IN_PROJECT=1 \
    pipenv install --deploy --ignore-pipfile --system


FROM python:3.14-alpine
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=0 

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.14/site-packages /usr/local/lib/python3.14/site-packages
COPY main.py .

RUN addgroup -S appgroup && \
    adduser -S appuser -G appgroup && \
    chown -R appuser:appgroup /app

USER appuser

COPY main.py .

CMD ["python", "main.py"]